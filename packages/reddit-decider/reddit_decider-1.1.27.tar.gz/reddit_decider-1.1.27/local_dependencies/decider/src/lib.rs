//! Decider is a library for determining whether a given feature should be available
//! in a given context.  It supports a very expressive set of operations for determining
//! which features should be available (and in what variant, if more than one is desired)
//! in a context.
extern crate crypto;

use std::collections::HashMap;
use std::fmt;
use std::fs::File;
use std::io::BufReader;

use num_bigint::BigUint;
use serde::{Deserialize, Serialize};
use serde_json::Value;

use self::crypto::digest::Digest;
use self::crypto::sha1::Sha1;

/// A context captures the relevant state in which we want to find out whether a feature
/// should be available.
#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub struct Context {
    pub user_id: Option<String>,

    /// IETF language tag representing the preferred locale for the client, used for
    /// providing localized content. Consists of an ISO 639-1 primary language subtag and
    /// an optional ISO 3166-1 alpha-2 region subtag separated by an underscore.
    ///
    /// e.g. `en`, `en_US`.
    pub locale: Option<String>,

    /// A two-character ISO 3166-1 country code.
    ///
    /// e.g. `US`.
    pub country_code: Option<String>,
    pub device_id: Option<String>,
    pub canonical_url: Option<String>,
    pub origin_service: Option<String>,
    pub user_is_employee: Option<bool>,
    pub logged_in: Option<bool>,
    pub app_name: Option<String>,
    pub build_number: Option<i32>,
    pub auth_client_id: Option<String>,
    pub cookie_created_timestamp: Option<f64>,
    pub other_fields: Option<HashMap<String, Value>>,
}

fn context_for_bucket_val(bv: &BucketVal, s: String) -> Context {
    Context {
        user_id: match bv {
            BucketVal::UserId => Some(s.clone()),
            _ => None,
        },
        locale: None,
        device_id: match bv {
            BucketVal::DeviceId => Some(s.clone()),
            _ => None,
        },
        country_code: None,
        canonical_url: match bv {
            BucketVal::CanonicalUrl => Some(s),
            _ => None,
        },
        ..Context::default()
    }
}

fn set_bucket_val(ctx: &Context, bucket_val: &BucketVal, s: String) -> Context {
    let mut out = ctx.clone();
    match bucket_val {
        BucketVal::UserId => out.user_id = Some(s),
        BucketVal::DeviceId => out.device_id = Some(s),
        &BucketVal::CanonicalUrl => out.canonical_url = Some(s),
    }
    out
}

impl Context {
    fn get_field(&self, field: &str) -> Result<Value, String> {
        let v: Option<Value> = match field {
            "user_id" => self.user_id.clone().map(Value::from),
            "device_id" => self.device_id.clone().map(Value::from),
            "canonical_url" => self.canonical_url.clone().map(Value::from),
            "locale" => self.locale.clone().map(Value::from),
            "country_code" => self.country_code.clone().map(Value::from),
            "origin_service" => self.origin_service.clone().map(Value::from),
            "app_name" => self.app_name.clone().map(Value::from),
            "user_is_employee" => self.user_is_employee.map(Value::from),
            "logged_in" => self.logged_in.map(Value::from),
            "build_number" => self.build_number.map(Value::from),
            "cookie_created_timestamp" => self.cookie_created_timestamp.map(Value::from),
            "auth_client_id" => self.auth_client_id.clone().map(Value::from),
            k => self.other_fields.as_ref().and_then(|m| m.get(k).cloned()),
        };
        v.ok_or(format!("missing field '{}'", field))
    }

    fn field_to_int(&self, name: &str) -> Result<i64, String> {
        match self.get_field(name) {
            Err(e) => Err(e),
            Ok(Value::Number(n)) => match n.as_i64() {
                None => Err("failed to get int".to_string()),
                Some(i) => Ok(i),
            },
            Ok(Value::String(s)) => match s.parse::<i64>() {
                Err(_) => Err("failed to parse string to int".to_string()),
                Ok(i) => Ok(i),
            },
            Ok(v) => Err(format!("value '{}' not a String or Number", v)),
        }
    }

    fn get_bucketing_field(&self, bucket_val: Option<&BucketVal>) -> Result<String, DeciderError> {
        match bucket_val {
            None => Err(DeciderError::MissingBucketVal),
            Some(bv) => match bv {
                BucketVal::UserId => match &self.user_id {
                    Some(u_id) => Ok(u_id.clone()),
                    None => Err(DeciderError::MissingBucketValInContext(
                        "user_id".to_string(),
                    )),
                },
                BucketVal::DeviceId => match &self.device_id {
                    Some(d_id) => Ok(d_id.clone()),
                    None => Err(DeciderError::MissingBucketValInContext(
                        "device_id".to_string(),
                    )),
                },
                BucketVal::CanonicalUrl => match &self.canonical_url {
                    Some(c_url) => Ok(c_url.clone()),
                    None => Err(DeciderError::MissingBucketValInContext(
                        "canonical_url".to_string(),
                    )),
                },
            },
        }
    }

    fn cmp(&self, field: &str, value: &Value) -> Result<bool, String> {
        match self.get_field(field) {
            Err(e) => Err(e),
            Ok(v) => value_eq(&v, value),
        }
    }

    fn cmp_op(&self, comp: Comp, field_name: &str, value: i64) -> Result<bool, String> {
        // GT/LT and friends only really make sense on Numbers, but sometimes might
        // show up as Strings in the experiment_config.json
        Ok(comp.cmp_ints(self.field_to_int(field_name)?, value))
    }
}

fn value_eq(x: &Value, y: &Value) -> Result<bool, String> {
    // will take in 2 Value objects, possibly of different Value::variants,
    // and do an equality test on them.  does string-> number conversion.
    match (&x, &y) {
        (Value::Null, _) => Ok(y.is_null()),
        (Value::Bool(b1), Value::Bool(b2)) => Ok(b1 == b2),
        (Value::String(s1), Value::String(s2)) => Ok(s1 == s2),
        (Value::String(s1), Value::Number(n2)) => Ok(s1 == &n2.to_string()),
        (Value::Number(n1), Value::Number(n2)) => Ok(n1 == n2),
        (Value::Number(n1), Value::String(s2)) => Ok(s2 == &n1.to_string()),
        _ => Err(format!("cannot compare '{:#?}' vs. '{:#?}'", x, y)),
    }
}

/// Features represent a unit of controllable code, that we might want to turn off, make
/// available only to some users, etc..  This is what FeatureFlags/AB tests control.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Feature {
    id: u32,
    name: String,
    enabled: bool,
    version: u32,
    owner: String,
    emit_event: bool,
    platform_bitmask: u64, // TODO: should this be made a vec for unbounded size?
    value: Option<Value>,
    targeting: Option<TargetingTree>,
    overrides: Option<Vec<HashMap<String, TargetingTree>>>,
    variant_set: Option<VariantSet>,
}

impl Feature {
    fn event_vector(
        &self,
        dt: DecisionKind,
        variant_name: String,
        ctx: &Context,
    ) -> Result<Vec<String>, DeciderError> {
        if self.emit_event {
            Ok(vec![self.event_string(dt, variant_name, ctx)?])
        } else {
            Ok(vec![])
        }
    }

    fn event_string(
        &self,
        dt: DecisionKind,
        variant_name: String,
        ctx: &Context,
    ) -> Result<String, DeciderError> {
        let vs = &self
            .variant_set
            .clone()
            .ok_or(DeciderError::MissingVariantSet)?;

        let opt_bucket_val = &vs.bucket_val;
        let bv = ctx.get_bucketing_field(opt_bucket_val.as_ref())?;
        let bucket_val = opt_bucket_val
            .clone()
            .ok_or(DeciderError::MissingBucketVal)?;

        Ok(format!(
            "{}::::{}::::{}::::{}::::{}::::{}::::{}::::{}::::{}::::{}",
            dt as u8,
            self.id,
            self.name,
            self.version,
            variant_name,
            bv,
            bucket_val,
            vs.start_ts,
            vs.stop_ts,
            self.owner
        ))
    }
}

#[derive(Copy, Clone)]
enum DecisionKind {
    FracAvail = 0,
    Override = 1,
    Holdout = 2,
    MutexGroup = 3,
}

impl DecisionKind {
    fn cast_event(&self, mut event_data: Vec<String>) -> Vec<String> {
        if event_data.is_empty() {
            event_data
        } else {
            let s = event_data[0].clone();
            let mut sv: Vec<String> = s.split(':').map(|s| s.to_string()).collect();
            sv[0] = format!("{}", *self as u8);
            event_data[0] = sv.join(":");
            event_data
        }
    }
}

/// VariantSet contains an experiment's variants, and all other fields not in common
/// with dynamic config json.
#[derive(Serialize, Deserialize, Debug, Clone)]
struct VariantSet {
    start_ts: u64, // TODO: consider whether this should just be created_at
    stop_ts: u64,  // TODO: should we get rid of a version by creating a new one?
    shuffle_version: u32,
    bucket_val: Option<BucketVal>,
    variants: Vec<Variant>,
    holdout: Option<Box<Feature>>,
    mutex_group: Option<Box<Feature>>,
}

/// Variants are primarily used for fractional availability, where, eg., 10% of users
/// are exposed to a given version of a feature.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Variant {
    name: String,
    #[serde(rename = "range_start")] // TODO change to alias and remove
    lo: f32, // consider changing away from floats.
    #[serde(rename = "range_end")]
    hi: f32,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct EqMany {
    field: String,
    values: Vec<Value>,
}

impl EqMany {
    fn eval(&self, ctx: &Context) -> Result<bool, String> {
        let x = ctx.get_field(&self.field)?; // Let's not fetch lots of times.
        let items: Result<Vec<bool>, String> =
            self.values.iter().map(|v| value_eq(&x, v)).collect();
        Ok(items?.iter().any(|&b| b))
    }
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct EqOne {
    field: String,
    value: Value,
}

impl EqOne {
    fn eval(&self, ctx: &Context) -> Result<bool, String> {
        ctx.cmp(&self.field, &self.value)
    }
}

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(untagged)]
pub enum EqEnum {
    EqOne(EqOne),
    EqMany(EqMany),
}

impl EqEnum {
    fn eval(&self, ctx: &Context) -> Result<bool, String> {
        match self {
            EqEnum::EqOne(eo) => eo.eval(ctx),
            EqEnum::EqMany(em) => em.eval(ctx),
        }
    }
}

/// The TargetingTree allows for arbitrary targeting operations, which can be used to
/// limit an experiment to employees, or users from New Zealand, only to iOS users, etc...
#[derive(Serialize, Deserialize, Debug, Clone)]
pub enum TargetingTree {
    ALL(Vec<TargetingTree>),
    ANY(Vec<TargetingTree>),
    NOT(Box<TargetingTree>),
    //#[serde(flatten)]
    EQ(EqEnum),
    GT { field: String, value: i64 },
    LT { field: String, value: i64 },
    GE { field: String, value: i64 },
    LE { field: String, value: i64 },
    NE { field: String, value: Value },
}

enum Comp {
    GT,
    LT,
    GE,
    LE,
}

impl Comp {
    fn cmp_ints(&self, i1: i64, i2: i64) -> bool {
        match self {
            Comp::GT => i1 > i2,
            Comp::LT => i1 < i2,
            Comp::GE => i1 >= i2,
            Comp::LE => i1 <= i2,
        }
    }
}
impl TargetingTree {
    fn eval(&self, ctx: &Context) -> Result<bool, String> {
        match self {
            TargetingTree::ALL(xs) => {
                let items: Result<Vec<bool>, String> = xs.iter().map(|x| x.eval(ctx)).collect();
                Ok(items?.iter().all(|&b| b))
            }
            TargetingTree::ANY(xs) => {
                let items: Result<Vec<bool>, String> = xs.iter().map(|x| x.eval(ctx)).collect();
                Ok(items?.iter().any(|&b| b))
            }
            TargetingTree::NOT(x) => Ok(!(x.eval(ctx)?)),
            TargetingTree::EQ(es) => es.eval(ctx),
            TargetingTree::GT { field, value } => ctx.cmp_op(Comp::GT, field, *value),
            TargetingTree::LT { field, value } => ctx.cmp_op(Comp::LT, field, *value),
            TargetingTree::GE { field, value } => ctx.cmp_op(Comp::GE, field, *value),
            TargetingTree::LE { field, value } => ctx.cmp_op(Comp::LE, field, *value),
            TargetingTree::NE { field, value } => Ok(!(ctx.cmp(field, value)?)),
        }
    }
}

/// Decider determines feature availability by chaining together simple decision maker
/// functions to enable complicated logic to be expressed as a composition of simple,
/// testable functions. Those compositions are tested against features, an abstraction
/// for bits of code that enabling feature flagging, AB testing, etc..
pub struct Decider {
    features: Vec<Feature>,
    decisionmakers: Vec<Decisionmaker>,
}

impl fmt::Debug for Decider {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Decider: {:#?}", self.features)
    }
}

impl Decider {
    pub fn choose(
        &self,
        feature_name: String,
        ctx: &Context,
    ) -> Result<Option<Decision>, DeciderError> {
        let f = self.feature_by_name(feature_name)?;
        self.decide(&f, ctx)
    }

    pub fn choose_all(
        &self,
        ctx: &Context,
    ) -> HashMap<String, Result<Option<Decision>, DeciderError>> {
        // FIXME: set this up such that we can filter by bucketing platform
        self.features
            .iter()
            .map(|f| (f.name.clone(), self.decide(f, ctx)))
            .collect()
    }

    pub fn choose_for(
        &self,
        feature_name: String,
        s: String,
        ctxo: &Option<Context>,
    ) -> Result<Option<Decision>, DeciderError> {
        let f = self.feature_by_name(feature_name)?;
        match (ctxo, f.variant_set.clone()) {
            (Some(ctx), None) => self.decide(&f, ctx),
            (Some(ctx), Some(vs)) => match &vs.bucket_val {
                Some(bv) => {
                    let ctxn = set_bucket_val(ctx, bv, s);
                    self.decide(&f, &ctxn)
                }
                None => Err(DeciderError::InvalidFeature),
            },
            (None, Some(vs)) => match &vs.bucket_val {
                Some(bv) => self.decide(&f, &context_for_bucket_val(bv, s)),
                None => Err(DeciderError::InvalidFeature),
            },
            (None, None) => Err(DeciderError::InvalidFeature),
        }
    }

    pub fn get_bool(&self, feature_name: String, ctx: &Context) -> Result<bool, DeciderError> {
        match self.get_value(feature_name, ctx) {
            Ok(Value::Bool(b)) => Ok(b),
            Ok(_) => Err(DeciderError::DcTypeMismatch),
            Err(e) => Err(e),
        }
    }

    pub fn get_int(&self, feature_name: String, ctx: &Context) -> Result<i64, DeciderError> {
        match self.get_value(feature_name, ctx) {
            Ok(Value::Number(n)) => match n.as_i64() {
                Some(int) => Ok(int),
                _ => Err(DeciderError::NumberDeserializationError),
            },
            Ok(_) => Err(DeciderError::DcTypeMismatch),
            Err(e) => Err(e),
        }
    }

    pub fn get_float(&self, feature_name: String, ctx: &Context) -> Result<f64, DeciderError> {
        match self.get_value(feature_name, ctx) {
            Ok(Value::Number(n)) => match n.as_f64() {
                Some(float) => Ok(float),
                _ => Err(DeciderError::NumberDeserializationError),
            },
            Ok(_) => Err(DeciderError::DcTypeMismatch),
            Err(e) => Err(e),
        }
    }

    pub fn get_string(&self, feature_name: String, ctx: &Context) -> Result<String, DeciderError> {
        match self.get_value(feature_name, ctx) {
            Ok(Value::String(s)) => Ok(s),
            Ok(_) => Err(DeciderError::DcTypeMismatch),
            Err(e) => Err(e),
        }
    }

    pub fn get_map(
        &self,
        feature_name: String,
        ctx: &Context,
    ) -> Result<serde_json::Map<String, Value>, DeciderError> {
        match self.get_value(feature_name, ctx) {
            Ok(Value::Object(obj)) => Ok(obj),
            Ok(_) => Err(DeciderError::DcTypeMismatch),
            Err(e) => Err(e),
        }
    }

    pub fn get_value(&self, feature_name: String, ctx: &Context) -> Result<Value, DeciderError> {
        let f = self.feature_by_name(feature_name)?;
        match self.decide(&f, ctx) {
            Err(e) => Err(e),
            Ok(None) => Err(DeciderError::InvalidFeature),
            Ok(Some(Decision {
                name: _,
                value,
                event_data: _,
                feature_id: _,
                feature_name: _,
                feature_version: _,
            })) => Ok(value),
        }
    }

    pub fn feature_by_name(&self, feature_name: String) -> Result<Feature, DeciderError> {
        match self.features.iter().find(|f| f.name == feature_name) {
            None => Err(DeciderError::FeatureNotFoundWithName(feature_name)),
            Some(feature) => Ok(feature.clone()),
        }
    }

    fn decide(&self, f: &Feature, ctx: &Context) -> Result<Option<Decision>, DeciderError> {
        // TODO: decide whether decide should return a Result<Option<Decision>>, to
        //       account for ill-defined Features or missing data on the Context. Probably
        //       yes, but currently Decision also has an option on name/bucketing.  Maybe
        //       decide should return a Result<Decision>?
        let mut out: Vec<String> = vec![];
        for fun in &self.decisionmakers {
            match fun(self, f, ctx)? {
                Choice::None => return Ok(None),
                Choice::Pass(_s) => (),
                Choice::Continue(d) => out.extend(d.event_data.clone()),
                Choice::Decided(mut d) => {
                    if !out.is_empty() {
                        out.extend(d.event_data);
                        d.event_data = out;
                    }
                    return Ok(Some(d));
                }
            }
        }
        Ok(None)
    }

    fn holdout(&self, f: &Feature, ctx: &Context) -> Result<Choice, DeciderError> {
        let hgo: &Option<Feature> = &f // This gets an Option<Feature>
            .variant_set
            .clone()
            .and_then(|vs| vs.holdout.map(|x| *x)); // open the Box
        match hgo {
            None => Ok(Choice::Pass("no_holdout_group".to_string())),
            Some(hg) => match self.decide(hg, ctx) {
                Err(e) => Err(e),
                Ok(None) => Ok(Choice::Pass("in_holdout:false".to_string())),
                Ok(Some(d)) => match d.name {
                    None => Ok(Choice::Pass("in_holdout:false".to_string())),
                    Some(s) => match s.as_str() {
                        "control_1" => Ok(Choice::Continue(Decision {
                            name: Some("control_1".to_string()),
                            value: Value::Null, // We don't need the actual value, as we'll end up in a diff exp.
                            event_data: DecisionKind::Holdout.cast_event(d.event_data),
                            feature_id: f.id,
                            feature_name: f.name.to_string(),
                            feature_version: f.version,
                        })),
                        "holdout" => Ok(Choice::Decided(Decision {
                            name: None,
                            value: hg.value.clone().unwrap_or_default(),
                            event_data: DecisionKind::Holdout.cast_event(d.event_data),
                            feature_id: f.id,
                            feature_name: f.name.to_string(),
                            feature_version: f.version,
                        })),
                        _ => Ok(Choice::Pass("in_holdout:false".to_string())),
                    },
                },
            },
        }
    }

    fn mutex_group(&self, f: &Feature, ctx: &Context) -> Result<Choice, DeciderError> {
        let mgo: &Option<Feature> = &f
            .variant_set
            .clone()
            .and_then(|vs| vs.mutex_group.map(|x| *x)); // open the Box
        match mgo {
            None => Ok(Choice::Pass("no_mutex_group".to_string())),
            Some(mg) => match self.decide(mg, ctx) {
                Err(e) => Err(e),
                Ok(None) => Ok(Choice::None), // I'm not in the mutex group exp.
                Ok(Some(Decision {
                    name: Some(s),
                    value: _,
                    event_data: ed,
                    feature_id: _,
                    feature_name: _,
                    feature_version: _,
                })) => {
                    // I got a decision!  But am I in the experiment I was asked for?
                    if s == f.name {
                        // Yes.  yes I am.  Let control flow through to the experiments
                        Ok(Choice::Continue(Decision {
                            name: Some(s),
                            value: Value::Null,
                            event_data: DecisionKind::MutexGroup.cast_event(ed),
                            feature_id: f.id,
                            feature_name: f.name.to_string(),
                            feature_version: f.version,
                        }))
                    } else {
                        // not in exp, terminate early.
                        Ok(Choice::None)
                    }
                }
                _ => Ok(Choice::None),
            },
        }
    }

    fn darkmode(&self, f: &Feature, _ctx: &Context) -> Result<Choice, DeciderError> {
        if f.enabled {
            Ok(Choice::Pass("darkmode:enabled".to_string()))
        } else {
            Ok(Choice::None)
        }
    }

    fn locale(&self, f: &Feature, _ctx: &Context) -> Result<Choice, DeciderError> {
        if !f.enabled {
            // TODO: add locales to Feature, compare ctx.locale to that
            Ok(Choice::Pass("locale:fixme".to_string()))
        } else {
            Ok(Choice::Pass("locale:fixme2".to_string()))
        }
    }

    fn fractional_availability(&self, f: &Feature, ctx: &Context) -> Result<Choice, DeciderError> {
        match &f.variant_set {
            None => Ok(Choice::Pass("frac_avail:no variant_set".to_string())),
            Some(vs) => vs.get_bucket(f, ctx),
        }
    }

    fn overrides(&self, f: &Feature, ctx: &Context) -> Result<Choice, DeciderError> {
        match &f.overrides {
            None => Ok(Choice::Pass("overrides:none_found".to_string())),
            Some(ov) => {
                for hm in ov.iter() {
                    for (name, tt) in hm.iter() {
                        match tt.eval(ctx) {
                            Err(s) => {
                                // FIXME: propagate the error and continue
                                return Ok(Choice::Pass(format!("t.eval err:{}", s)));
                            }
                            Ok(true) => {
                                return Ok(Choice::Decided(Decision {
                                    // FIXME: check to make sure this is a variant name
                                    name: Some(name.clone()),
                                    value: Value::String(name.clone()),
                                    event_data: f.event_vector(
                                        DecisionKind::Override,
                                        name.clone(),
                                        ctx,
                                    )?,
                                    feature_id: f.id,
                                    feature_name: f.name.to_string(),
                                    feature_version: f.version,
                                }));
                            }
                            Ok(false) => continue,
                        }
                    }
                }
                Ok(Choice::Pass("overrides:none_hit".to_string()))
            }
        }
    }

    fn targeting(&self, f: &Feature, ctx: &Context) -> Result<Choice, DeciderError> {
        match &f.targeting {
            None => Ok(Choice::Pass("targeting:none_found".to_string())),
            Some(tt) => match tt.eval(ctx) {
                Err(_) => Ok(Choice::None), // FIXME: propagate the error
                Ok(true) => Ok(Choice::Pass("targeting:targeted".to_string())),
                Ok(false) => Ok(Choice::None),
            },
        }
    }

    fn value(&self, f: &Feature, _ctx: &Context) -> Result<Choice, DeciderError> {
        match &f.value {
            None => Ok(Choice::None),
            Some(value) => match value {
                Value::Null | Value::Array(_) => {
                    Ok(Choice::Pass("value:null_or_array".to_string()))
                }
                _ => Ok(Choice::Decided(Decision {
                    name: None,
                    value: value.clone(),
                    event_data: vec![],
                    feature_id: f.id,
                    feature_name: f.name.to_string(),
                    feature_version: f.version,
                })),
            },
        }
    }
}

impl VariantSet {
    fn bucketing_string(&self, exp_id: &u32, name: &str, identifier: &str) -> String {
        format!("{}.{}.{}{}", exp_id, name, self.shuffle_version, identifier)
    }

    fn get_bucket(&self, f: &Feature, ctx: &Context) -> Result<Choice, DeciderError> {
        let identifier = ctx.get_bucketing_field(self.bucket_val.as_ref())?;
        let bucketing_string = self.bucketing_string(&f.id, &f.name, &identifier);
        let i = bucket(&bucketing_string)?;
        let flt = (i as f32) / 1000.0;
        let v = self.variants.iter().find(|x| x.lo <= flt && x.hi > flt);
        match v {
            None => Ok(Choice::Pass("frac_avail:not in variants".to_string())),
            Some(variant) => Ok(Choice::Decided(Decision {
                name: Some(variant.name.clone()),
                value: Value::Null,
                event_data: f.event_vector(DecisionKind::FracAvail, variant.name.clone(), ctx)?,
                feature_id: f.id,
                feature_name: f.name.to_string(),
                feature_version: f.version,
            })),
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Choice {
    // TODO: find a better nome
    Pass(String),       // I didn't make a decision because...
    None,               // response is nothing
    Continue(Decision), // a parent decision got called, so save that and continue
    Decided(Decision),  // actual decision.
}

#[derive(Debug)]
pub enum DeciderError {
    FeatureNotFound,
    FeatureNotFoundWithName(String),
    InvalidFeature,
    MissingBucketVal,
    MissingBucketValInContext(String),
    BucketingError(String),
    MissingVariantSet,
    DcTypeMismatch,
    NumberDeserializationError,
    MapDeserializationError(String),
}

#[derive(Debug)]
pub enum DeciderInitError {
    IoError(std::io::Error),
    SerdeError(serde_json::Error),
    InvalidDecisionMaker(String),
}

impl fmt::Display for DeciderError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &*self {
            DeciderError::FeatureNotFound => write!(f, "Feature not found."),
            DeciderError::FeatureNotFoundWithName(name) => {
                write!(f, "Feature {:#?} not found.", name)
            }
            DeciderError::InvalidFeature => write!(f, "Invalid Feature configuration."),
            DeciderError::BucketingError(s) => write!(f, "{}", s),
            DeciderError::MissingBucketVal => {
                write!(f, "Missing \"bucket_val\" field in experiment config.")
            }
            DeciderError::MissingBucketValInContext(bucket_val) => write!(
                f,
                "Missing {:#?} in context for bucket_val = {:#?}",
                bucket_val, bucket_val
            ),
            DeciderError::MissingVariantSet => write!(f, "Missing variant_set"),
            DeciderError::DcTypeMismatch => {
                write!(f, "Dynamic Configuration Feature type mismatch.")
            }
            DeciderError::NumberDeserializationError => {
                write!(f, "Number deserialization failed.")
            }
            DeciderError::MapDeserializationError(err_str) => {
                write!(f, "Map deserialization failed: {:#?}", err_str)
            }
        }
    }
}

impl fmt::Display for DeciderInitError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &*self {
            DeciderInitError::InvalidDecisionMaker(err_str) => {
                write!(f, "Invalid DecisionMaker: {:#?}", err_str.clone())
            }
            DeciderInitError::SerdeError(serde_json_error) => {
                write!(f, "Json error: {:#?}", serde_json_error.to_string())
            }
            DeciderInitError::IoError(std_io_error) => {
                write!(f, "Std io error: {:#?}", std_io_error.to_string())
            }
        }
    }
}

impl From<std::io::Error> for DeciderInitError {
    fn from(e: std::io::Error) -> DeciderInitError {
        DeciderInitError::IoError(e)
    }
}

impl From<serde_json::Error> for DeciderInitError {
    fn from(e: serde_json::Error) -> DeciderInitError {
        DeciderInitError::SerdeError(e)
    }
}

#[derive(PartialEq, Eq, Serialize, Deserialize, Debug, Clone)]
pub struct Decision {
    pub name: Option<String>,
    pub value: Value,
    pub event_data: Vec<String>,
    pub feature_id: u32,
    pub feature_name: String,
    pub feature_version: u32,
}

fn bucket(bucketing_str: &str) -> Result<i32, DeciderError> {
    // FIXME: take in number of buckets as a param.
    let mut hasher = Sha1::new();
    hasher.input_str(bucketing_str);
    let bigint_opt = BigUint::parse_bytes(hasher.result_str().as_bytes(), 16);
    let bigint_res = match bigint_opt {
        Some(v) => Ok(v % 1000u32),
        None => Err(DeciderError::BucketingError(format!(
            "'{}' failed",
            bucketing_str
        ))),
    };
    let i32_res: Result<i32, _> = bigint_res?.try_into();
    match i32_res {
        Ok(i) => Ok(i),
        Err(_) => Err(DeciderError::BucketingError("bigint fail".to_string())),
    }
}

type Decisionmaker = fn(d: &Decider, f: &Feature, ctx: &Context) -> Result<Choice, DeciderError>;

fn name_to_decisionmaker(name: &str) -> Result<Decisionmaker, String> {
    return match name {
        "darkmode" => Ok(Decider::darkmode),
        "locale" => Ok(Decider::locale),
        "fractional_availability" => Ok(Decider::fractional_availability),
        "targeting" => Ok(Decider::targeting),
        "overrides" => Ok(Decider::overrides),
        "value" => Ok(Decider::value),
        "holdout" => Ok(Decider::holdout),
        "mutex_group" => Ok(Decider::mutex_group),
        _ => Err(format!("Invalid decisionmaker name: {:?}", name)),
    };
}

fn string_to_decisionmakers(cfg: String) -> Result<Vec<Decisionmaker>, String> {
    // we get a result of a vec because we want any single error in
    // decisionmaker names to fail the whole thing (no silent errors
    // causing unexpected behavior).  Got the technique from:
    // https://stackoverflow.com/questions/26368288/how-do-i-stop-iteration-and-return-an-error-when-iteratormap-returns-a-result
    cfg.split_whitespace().map(name_to_decisionmaker).collect()
}

pub fn init(cfg: String, features: Vec<Feature>) -> Result<Decider, DeciderInitError> {
    match string_to_decisionmakers(cfg) {
        Ok(decisionmakers) => Ok(Decider {
            features,
            decisionmakers,
        }),
        Err(s) => Err(DeciderInitError::InvalidDecisionMaker(s)),
    }
}

// This section is legacy code to deal with reddit's existing experiment format.
pub fn init_decider(cfg: String, filepath: String) -> Result<Decider, DeciderInitError> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let ec: ExperimentConfig = serde_json::from_reader(reader)?;
    let fl = experiment_config_to_features(ec)?;
    init(cfg, fl)
}

fn experiment_config_to_features(ec: ExperimentConfig) -> Result<Vec<Feature>, DeciderInitError> {
    let ec2 = ec.clone();
    let fl: Vec<Feature> = ec
        .into_values()
        .map(|exp| experiment_to_feature(&exp, &ec2))
        .collect();
    Ok(fl)
}

type ExperimentConfig = HashMap<String, Experiment>;

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Experiment {
    id: u32,
    name: String,
    enabled: bool,
    version: String,
    owner: String,
    #[serde(rename = "type")]
    experiment_type: ExperimentType,
    #[serde(default)]
    emit_event: bool,
    #[serde(default)]
    start_ts: u64,
    #[serde(default)]
    stop_ts: u64,
    value: Option<Value>, // used by dynamic_config
    parent_meg_name: Option<String>,
    parent_hg_name: Option<String>,
    experiment: InnerExperiment,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(rename_all(deserialize = "snake_case"))]
enum ExperimentType {
    DynamicConfig,
    RangeVariant,
    FeatureRollout, // FIXME: get rid of this after the great RangeVariant takeover.
}

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(rename_all(deserialize = "snake_case"))]
enum BucketVal {
    #[serde(rename = "user_id")]
    UserId,
    #[serde(rename = "device_id")]
    DeviceId,
    #[serde(rename = "canonical_url")]
    CanonicalUrl,
}

impl fmt::Display for BucketVal {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            BucketVal::UserId => {
                write!(f, "user_id")
            }
            BucketVal::DeviceId => {
                write!(f, "device_id")
            }
            BucketVal::CanonicalUrl => {
                write!(f, "canonical_url")
            }
        }
    }
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct InnerExperiment {
    experiment_version: u32,
    #[serde(default)]
    variants: Vec<Variant>, // TODO: figure out how to make a variable-length array in a struct, maybe?
    #[serde(default)]
    shuffle_version: u32,
    bucket_val: Option<BucketVal>,
    overrides: Option<Vec<HashMap<String, TargetingTree>>>,
    targeting: Option<TargetingTree>,
}

fn experiment_to_feature(exp: &Experiment, ec: &ExperimentConfig) -> Feature {
    let holdout: Option<Box<Feature>> = match &exp.parent_hg_name {
        None => None,
        Some(name) => ec.get(name).map(|e| Box::new(experiment_to_feature(e, ec))),
    };

    let mutex_group = match &exp.parent_meg_name {
        None => None,
        Some(name) => ec.get(name).map(|e| Box::new(experiment_to_feature(e, ec))),
    };

    let variant_set = match exp.experiment_type {
        ExperimentType::DynamicConfig => None,
        _ => Some(VariantSet {
            start_ts: exp.start_ts,
            stop_ts: exp.stop_ts,
            shuffle_version: exp.experiment.shuffle_version,
            variants: exp.experiment.variants.clone(),
            bucket_val: exp.experiment.bucket_val.clone(),
            holdout,
            mutex_group,
        }),
    };

    Feature {
        id: exp.id,
        name: exp.name.clone(),
        enabled: exp.enabled,
        version: exp.experiment.experiment_version,
        owner: exp.owner.clone(),
        platform_bitmask: 0,
        value: exp.value.clone(),
        emit_event: exp.emit_event,
        targeting: exp.experiment.targeting.clone(),
        overrides: exp.experiment.overrides.clone(),
        variant_set,
    }
}

#[cfg(test)]
mod tests {
    use proptest::prelude::*;
    use serde_json::json;
    use serde_json::Error;

    use super::*;

    enum Dc {
        Bool(Option<Value>),
        Int(Option<Value>),
        Float(Option<Value>),
        String(Option<Value>),
        Map(Option<String>),
    }

    fn make_feature() -> Feature {
        let v = Variant {
            name: "enabled".to_string(),
            lo: 0.0,
            hi: 0.1,
        };
        Feature {
            id: 1,
            name: "first_feature".to_string(),
            enabled: true,
            version: 1,
            owner: "test".to_string(),
            platform_bitmask: 0,
            emit_event: true,
            targeting: None,
            overrides: None,
            variant_set: Some(VariantSet {
                start_ts: 0,
                stop_ts: 2147483648, // 2 ** 31 - far future.
                shuffle_version: 0,
                bucket_val: Some(BucketVal::UserId),
                variants: vec![v],
                holdout: None,
                mutex_group: None,
            }),
            value: Some(Value::Null),
        }
    }

    fn make_dynamic_config(dc: Dc) -> Feature {
        let name_str: String;

        let value: Value = match dc {
            Dc::Bool(val) => {
                name_str = "bool".to_string();
                match val {
                    None => Value::Bool(true),
                    Some(b) => b,
                }
            }
            Dc::Int(val) => {
                name_str = "int".to_string();
                match val {
                    None => Value::from(1),
                    Some(i) => i,
                }
            }
            Dc::Float(val) => {
                name_str = "float".to_string();
                match val {
                    None => Value::from(2.0),
                    Some(f) => f,
                }
            }
            Dc::String(val) => {
                name_str = "string".to_string();
                match val {
                    None => Value::from("some_string"),
                    Some(s) => s,
                }
            }
            Dc::Map(val) => {
                name_str = "map".to_string();
                match &val {
                    None => {
                        json!({"v":{"nested_map": {"w":false,"x": 1,"y":"some_string","z":3.0}},"w":false,"x": 1,"y":"some_string","z":3.0})
                    }
                    Some(s) => serde_json::from_str(s).unwrap(),
                }
            }
        };

        Feature {
            id: 2,
            name: name_str + "_dynamic_config",
            enabled: true,
            version: 1,
            owner: "test".to_string(),
            emit_event: true,
            value: Some(value),
            targeting: None,
            overrides: None,
            platform_bitmask: 0,
            variant_set: None,
        }
    }

    fn make_experiment(name: String, meg: Option<String>, hg: Option<String>) -> Experiment {
        let c = Variant {
            name: "control".to_string(),
            hi: 1.0,
            lo: 0.9,
        };
        let t = Variant {
            name: "treatment".to_string(),
            hi: 0.1,
            lo: 0.0,
        };
        Experiment {
            id: 1,
            name,
            experiment_type: ExperimentType::RangeVariant,
            enabled: true,
            owner: "test".to_string(),
            emit_event: true,
            start_ts: 0,
            stop_ts: 2147483648, // 2 ** 31 - far future.
            version: "1".to_string(),
            experiment: InnerExperiment {
                shuffle_version: 0,
                variants: vec![t, c],
                bucket_val: Some(BucketVal::UserId),
                experiment_version: 1,
                targeting: None,
                overrides: None,
            },
            parent_hg_name: hg,
            parent_meg_name: meg,
            value: None,
        }
    }

    fn make_ctx(json: Option<String>) -> Result<Context, Error> {
        let c = Context {
            user_id: Some("795244".to_string()),
            locale: Some("US".to_string()),
            ..Context::default()
        };
        match json {
            None => Ok(c),
            Some(s) => serde_json::from_str(&s),
        }
    }

    fn make_tt(json: String) -> TargetingTree {
        serde_json::from_str(&json).unwrap()
    }

    #[test]
    fn parse_targeting_tree() -> Result<(), String> {
        let tt1 = make_tt(r#"{"EQ": {"field": "user_id", "values": ["795244"]}}"#.to_string());
        let tt2 = make_tt(r#"{"EQ": {"field": "user_id", "value": "795244"}}"#.to_string());
        let tt3 = make_tt(r#"{"NE": {"field": "user_id", "value": "795244"}}"#.to_string());
        let tt4 = make_tt(r#"{"GT": {"field": "user_id", "value": 7}}"#.to_string());
        let tt5 = make_tt(r#"{"LT": {"field": "user_id", "value": 8}}"#.to_string());
        let tt6 = make_tt(r#"{"GE": {"field": "user_id", "value": 8}}"#.to_string());
        let tt7 = make_tt(r#"{"LE": {"field": "user_id", "value": 8}}"#.to_string());
        let tt8 = make_tt(r#"{"ALL": [{"EQ": {"field": "user_id", "value": 7}}]}"#.to_string());
        let tt9 = make_tt(r#"{"ALL": [{"EQ": {"field": "user_id", "value": "7"}}]}"#.to_string());
        let imp = make_tt(r#"{"ALL": [{"EQ": {"field": "user_id", "value": "7"}},{"EQ": {"field": "user_id", "value": "8"}}]}"#.to_string());
        let _big = make_tt(
            r#"{"ALL": [
          {"EQ": {"field": "country_code","values": ["DE"]}},
          {"ANY": [
              {"ALL": [
                  {"EQ": {"field": "app_name","value": "ios"}},
                  {"GE": {"field": "build_number","value": 307593}}
                ]
              },
              {"EQ": {"field": "app_name","value": "android"}}
            ]
          }
        ]
      }"#
            .to_string(),
        );

        let ctx1 = make_ctx(None).unwrap();
        let ctx2: Context = make_ctx(Some(r#"{"user_id": "7"}"#.to_string())).unwrap();
        let _ctx3: Context = make_ctx(Some(
            json!({"user_id": "9",
                   "user_is_employee": false,
                   "country_code": "DE",
                   "app_name": "android",
                   "build_number": 312024,
                   "logged_in": true,
            })
            .to_string(),
        ))
        .unwrap();

        assert!(tt1.eval(&ctx1)?); // ctx1 has user_id 795244, so EQ passes
        assert!(!tt1.eval(&ctx2)?); // ctx2 has user_id 7, so EQ fails
        assert!(tt2.eval(&ctx1)?); // tt1 and tt2 are the same, just different representations
        assert!(!tt2.eval(&ctx2)?); // so should have same results

        assert!(!tt3.eval(&ctx1)?); // ctx has user_id 795244, so NE against 795244 fails
        assert!(tt3.eval(&ctx2)?); // ctx2 has user_id 7, so NE against 7 passes

        assert!(tt4.eval(&ctx1)?); // ctx has user_id 795244, so GT against 7 passes
        assert!(!tt4.eval(&ctx2)?); // ctx2 has user_id 7, so GT against 7 fails

        assert!(!tt5.eval(&ctx1)?); // ctx has user_id 795244, so LT against 8 passes
        assert!(tt5.eval(&ctx2)?); // ctx2 has user_id 7, so LT against 8 fails

        assert!(tt6.eval(&ctx1)?); // ctx has user_id 795244, so GE against 8 passes
        assert!(!tt6.eval(&ctx2)?); // ctx2 has user_id 7, so GE against 8 fails

        assert!(!tt7.eval(&ctx1)?); // ctx has user_id 795244, so LE against 8 fails
        assert!(tt7.eval(&ctx2)?); // ctx2 has user_id 7, so LE against 8 passes

        // test {ALL: [{user_id: "7"} ]}
        assert!(!tt8.eval(&ctx1)?); // ctx1 has user_id 795244, so EQ fails, so ALL fails
        assert!(tt8.eval(&ctx2)?); // ctx2 has user_id 7, so EQ passes, so ALL passes

        // same as above, but literal int rather than string
        assert!(!tt9.eval(&ctx1)?); // ctx1 has user_id 795244, so EQ fails, so ALL fails
        assert!(tt9.eval(&ctx2)?); // ctx2 has user_id 7, so EQ passes, so ALL passes

        // an impossible targeting tree that asks us to have 2 different user_ids at once.
        assert!(!imp.eval(&ctx1)?); // ctx1 has user_id 795244, so both EQs fail
        assert!(!imp.eval(&ctx2)?); // ctx1 has user_id 7, so second EQ fails
        Ok(())
    }

    fn build_decider(
        cfgo: Option<String>,
        fvo: Option<Vec<Feature>>,
        dcvo: Option<Vec<Feature>>,
    ) -> Result<Decider, DeciderInitError> {
        let fv = match fvo {
            None => vec![make_feature()],
            Some(fv) => fv,
        };
        let dcv = match dcvo {
            None => vec![
                make_dynamic_config(Dc::Bool(None)),
                make_dynamic_config(Dc::Int(None)),
                make_dynamic_config(Dc::Float(None)),
                make_dynamic_config(Dc::String(None)),
                make_dynamic_config(Dc::Map(None)),
            ],
            Some(dc) => dc,
        };
        let cfg = match cfgo {
            Some(s) => s,
            None => "darkmode".to_string(), // set a reasonable default here?
        };
        init(cfg, [fv, dcv].concat())
    }

    #[test]
    fn decider_initialization_works() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(None, None, None)?;
        assert!(d.choose("first_feature".to_string(), &ctx).is_ok());
        Ok(())
    }

    #[test]
    fn decider_errors_on_missing_name() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(None, None, None)?;
        let r = d.choose("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn test_name_to_decisionmaker() -> Result<(), String> {
        name_to_decisionmaker("darkmode")?;
        name_to_decisionmaker("fractional_availability")?;
        name_to_decisionmaker("locale")?;
        name_to_decisionmaker("value")?;
        name_to_decisionmaker("overrides")?;
        name_to_decisionmaker("targeting")?;
        let res = name_to_decisionmaker("bad-shouldbreak");
        match res {
            Ok(_) => Err("obviously bad variant: bad-shouldbreak passed".to_string()),
            Err(_) => Ok(()),
        }
    }

    proptest! {
        #[test]
        fn init_decider_doesnt_crash(s in "\\PC*") {
            let res = init_decider(s, "../cfgsmall.json".to_string());
            match res {
                Ok(d) => println!("success: {:#?}", d),
                Err(e) => println!("error: {:#?}", e),
            }
        }

        #[test]
        fn no_user_id_can_pass_impossible_tt(i in 10..1000000000u64 ) {
            let v = json!({"user_id": i.to_string()});
            let imp = make_tt(r#"{"ALL": [{"EQ": {"field": "user_id", "value": "7"}},{"EQ": {"field": "user_id", "value": "8"}}]}"#.to_string());
            let ctx: Context = make_ctx(Some(v.to_string()))?;

            assert!(!imp.eval(&ctx).unwrap());
        }

        #[test]
        fn test_meg_hg_invariants(i in 1..1000000000u64) {
            let d = init_decider(
                "darkmode overrides targeting holdout mutex_group fractional_availability value".to_string(),
                "../test.json".to_string()).unwrap();

            let ctx: Context = make_ctx(
                Some(json!({"user_id": i.to_string()}).to_string())
            ).unwrap();

            // let's get all 4 test features bucketed, and out of their Results
            let hghalf = d.choose("hghalf".to_string(), &ctx).unwrap();
            let meg2way = d.choose("meg2way".to_string(), &ctx).unwrap();
            let e1 = d.choose("e1".to_string(), &ctx).unwrap();
            let e2 = d.choose("e2".to_string(), &ctx).unwrap();

            match (massage_holdout(hghalf), meg2way) {
                // If you're in the holdout, you don't get any experiments
                ((Some(true), ed), _) => both_no_name(e1, e2, ed),
                // Regardless of what's going on in the holdout, if the MEG
                // doesn't give any results, both decisions should have name=None
                ((_, ed), None) => both_no_name(e1, e2, ed),
                ((_, ed), Some(mg)) => {
                    match mg.name {
                        None => both_no_name(e1, e2, ed), // None == no exps! Shouldn't get here
                        Some(s) => one_off_one_on(e1, e2, s),
                    }
                },
            }
        }

        #[test]
        fn test_overrides(i in 6..1000000000u64) {
            let d = init_decider(
                "darkmode overrides targeting holdout mutex_group fractional_availability value".to_string(),
                "../test.json".to_string()).unwrap();
            let ctx1: Context = make_ctx(Some(
                json!({"user_id": (i * 10).to_string(), "user_is_employee": true}).to_string(),
            )).unwrap();

            let ctx2: Context = make_ctx(Some(
                json!({"user_id": (i * 10 + 1).to_string(),
                       "user_is_employee": false,
                       "country_code": "DE",
                       "app_name": "android",
                       "build_number": 312024,
                       "logged_in": true,
                }).to_string(),
            )).unwrap();

            let ctx3: Context = make_ctx(Some(
                json!({"user_id": (i * 10 + 2).to_string()}).to_string(),
            )).unwrap();

            let ctx4: Context = make_ctx(Some(
                json!({"user_id": (i * 10 + 3).to_string(),
                       "user_is_employee": false,
                       "country_code": "DE",
                       "app_name": "android",
                       "build_number": 312024,
                       "logged_in": true,
                }).to_string(),
            )).unwrap();

            println!("test 1");
            // ctx1 is an employee, so it'll get overridden into control in fancy, and never see holdout/meg
            let control = d.choose("fancy".to_string(), &ctx1).unwrap().unwrap();
            assert_eq!(control.name, Some("control".to_string()));
            assert_eq!(control.feature_id, 1);
            assert_eq!(control.feature_name, *"fancy");
            assert_eq!(control.feature_version, 4);
            assert_eq!(control.event_data, vec![format!("1::::1::::fancy::::4::::control::::{}::::user_id::::0::::9668199193::::test", i * 10)]);

            let x1 = d.choose("hg".to_string(), &ctx2).unwrap().unwrap();
            assert_eq!(x1.name, Some("control_1".to_string()));
            assert_eq!(x1.feature_id, 2);
            assert_eq!(x1.feature_name, *"hg");
            assert_eq!(x1.feature_version, 5);
            assert_eq!(x1.event_data, vec![format!("1::::2::::hg::::5::::control_1::::{}::::user_id::::0::::9668199193::::test", i * 10 + 1)]);

            let x2 = d.choose("meg".to_string(), &ctx2).unwrap().unwrap();
            assert_eq!(x2.name, Some("fancy".to_string()));
            assert_eq!(x2.feature_id, 3);
            assert_eq!(x2.feature_name, *"meg");
            assert_eq!(x2.feature_version, 7);
            // MEGs don't fire exposures since `emit_event` is false in test.json config
            let empty_vec: Vec<String> = vec![];
            assert_eq!(x2.event_data, empty_vec);

            println!("test 2");
            // ctx2 employee=false, so in fancy, "none_hit"s the overrides, passes targeting, goes to holdout-is in control(gets experiments).
            // Passes to the meg, it gets "fancy" treatment, which means it is eligible for this experiment, and gets frac_avail in enabled
            let exp1 = d.choose("fancy".to_string(), &ctx2).unwrap().unwrap();
            assert_eq!(exp1.name, Some("exp1".to_string()));
            assert_eq!(exp1.feature_id, 1);
            assert_eq!(exp1.feature_name, *"fancy");
            assert_eq!(exp1.feature_version, 4);
            println!("exp1.event_data={:#?}", exp1.event_data);
            assert_eq!(exp1.event_data, vec![
                format!("2::::2::::hg::::5::::control_1::::{}::::user_id::::0::::9668199193::::test", i * 10 + 1),
                format!("0::::1::::fancy::::4::::exp1::::{}::::user_id::::0::::9668199193::::test", i * 10 + 1)]);


            println!("test 3");
            // ctx3 isn't an employee, so misses overrides, and fails targeting, so gets nothing.
            assert!(d.choose("fancy".to_string(), &ctx3).unwrap().is_none());

            println!("test 4");
            // ctx4 employee=false, so in fancy, "none_hit"s the overrides,
            // passes targeting, goes to holdout-is in control(gets
            // experiments). Passes to the meg, it misses overrides and gets
            // frac_avail'd into the "fancy" treatment, which means it is
            // allowed into the "fancy" experiment, which in turn means it gets
            // bucketed.
            let fancy = d.choose("fancy".to_string(), &ctx4).unwrap().unwrap();
            println!("fancy={:#?}", fancy);
            assert_eq!(fancy.name, Some("exp1".to_string()));
            assert_eq!(fancy.feature_id, 1);
            assert_eq!(fancy.feature_name, *"fancy");
            assert_eq!(fancy.feature_version, 4);
            assert_eq!(fancy.event_data, vec![
                format!("2::::2::::hg::::5::::control_1::::{}::::user_id::::0::::9668199193::::test", i * 10 + 3),
                format!("0::::1::::fancy::::4::::exp1::::{}::::user_id::::0::::9668199193::::test", i * 10 + 3)]);
        }

        #[test]
        fn test_choose_all(i in 0..1000000000u64) {
            let filepath = "../test.json".to_string();
            let d = init_decider(
                "darkmode overrides targeting holdout mutex_group fractional_availability value".to_string(),
                filepath.clone()).unwrap();
            let ctx: Context = make_ctx(Some(
                json!({"user_id": i.to_string()}).to_string(),
            )).unwrap();

            let file = File::open(filepath)?;
            let reader = BufReader::new(file);
            let ec: ExperimentConfig = serde_json::from_reader(reader)?;
            let hm = d.choose_all(&ctx);
            // TODO: come up with something smarter to test here.
            for (k, v) in hm {
                match v {
                    Err(_) => panic!(), // We shouldn't see any errors
                    Ok(None) => (), // Normal not to have a decision
                    Ok(Some(d)) => { // if a decision has a name, must be from the variant names.
                        if let Some(name) = d.name { // IFF we got a decision, the names should match.
                            let exp_conf = ec.get(&k).unwrap();
                            assert!(exp_conf.experiment.variants.iter().any(|f| f.name == name));
                            assert!(exp_conf.id == d.feature_id);
                            assert!(exp_conf.experiment.experiment_version == d.feature_version);
                            assert!(exp_conf.name == d.feature_name);

                        }
                    }
                }
            }
        }
    }

    fn massage_holdout(hg: Option<Decision>) -> (Option<bool>, Vec<String>) {
        match hg {
            None => (None, vec![]),
            Some(Decision {
                name: n,
                value: _,
                event_data: ed,
                feature_id: _,
                feature_name: _,
                feature_version: _,
            }) => (Some(n == Some("holdout".to_string())), ed),
        }
    }

    fn both_no_name(e1: Option<Decision>, e2: Option<Decision>, _ed: Vec<String>) {
        assert!(e1.and_then(|d| d.name).is_none());
        assert!(e2.and_then(|d| d.name).is_none());
    }

    fn one_off_one_on(e1: Option<Decision>, e2: Option<Decision>, s: String) {
        // This function is highly specific: it depends on being called with
        // e1 == choose("e1") and e2 == choose("e2")
        match e1.is_none() {
            true => {
                assert_eq!(s, "e2".to_string());
                assert_eq!(e2.unwrap().name, Some("e2treat".to_string()));
            }
            false => {
                assert_eq!(s, "e1".to_string());
                assert_eq!(e1.unwrap().name, Some("e1treat".to_string()));
            }
        }
    }

    #[test]
    fn init_decider_works() -> Result<(), DeciderInitError> {
        init_decider(
            "darkmode overrides targeting fractional_availability value".to_string(),
            "../cfg.json".to_string(),
        )?;
        Ok(())
    }

    #[test]
    fn holdout_meg_parsing() -> Result<(), DeciderError> {
        let e1 = make_experiment(
            "first".to_string(),
            Some("meg".to_string()),
            Some("hg".to_string()),
        );
        let e2 = make_experiment(
            "second".to_string(),
            Some("meg_missing".to_string()),
            Some("hg".to_string()),
        );
        let meg = make_experiment("meg".to_string(), None, None);
        let hg = make_experiment("hg".to_string(), None, None);
        let ec: ExperimentConfig = HashMap::from([
            ("first".to_string(), e1),
            ("second".to_string(), e2),
            ("meg".to_string(), meg),
            ("hg".to_string(), hg),
        ]);

        let fv: Vec<Feature> = experiment_config_to_features(ec).unwrap();
        let f1 = fv.iter().find(|&f| f.name == "first").unwrap();
        let f2 = fv.iter().find(|&f| f.name == "second").unwrap();
        let fmeg = fv.iter().find(|&f| f.name == "meg").unwrap();
        let fhg = fv.iter().find(|&f| f.name == "hg").unwrap();
        assert_eq!(get_fp(f1, FeatureParent::Holdout)?.name, fhg.name);
        assert_eq!(get_fp(f1, FeatureParent::Meg)?.name, fmeg.name);
        assert!(get_fp(f2, FeatureParent::Meg).is_err());
        assert_eq!(get_fp(f2, FeatureParent::Holdout)?.name, fhg.name);
        assert!(get_fp(fmeg, FeatureParent::Holdout).is_err());
        assert!(get_fp(fmeg, FeatureParent::Meg).is_err());
        assert!(get_fp(fhg, FeatureParent::Holdout).is_err());
        assert!(get_fp(fhg, FeatureParent::Meg).is_err());
        Ok(())
    }

    enum FeatureParent {
        Meg,
        Holdout,
    }

    fn get_fp(f: &Feature, fp: FeatureParent) -> Result<Feature, DeciderError> {
        // grab the specified feature_parent(holdout or meg) from a feature, or err trying.
        if let Some(variant_set) = &f.variant_set {
            let fpo = match fp {
                FeatureParent::Meg => variant_set.mutex_group.clone(),
                FeatureParent::Holdout => variant_set.holdout.clone(),
            };
            match fpo {
                None => Err(DeciderError::FeatureNotFound),
                Some(feature_parent) => Ok(*feature_parent),
            }
        } else {
            Err(DeciderError::FeatureNotFound)
        }
    }

    #[test]
    fn get_bool_works() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;

        if let Ok(true) = d.get_bool("bool_dynamic_config".to_string(), &ctx) {
            println!("got expected boolean: true");
        } else {
            panic!();
        }

        Ok(())
    }

    #[test]
    fn get_bool_errors_on_missing_name() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_bool("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_int_works() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let dc_res = d.get_int("int_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == 1 {
                    println!("got expected int: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_int_errors_on_missing_name() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_int("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_float_works() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let dc_res = d.get_float("float_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == 2.0 {
                    println!("got expected float: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_float_errors_on_missing_name() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_float("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_string_works() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let dc_res = d.get_string("string_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == "some_string" {
                    println!("got expected string: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_string_errors_on_missing_name() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_string("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn get_map_works() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let map_dc_str = r#"{"v":{"nested_map": {"w":false,"x": 1,"y":"some_string","z":3.0}},"w":false,"x": 1,"y":"some_string","z":3.0}"#;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            Some(vec![make_dynamic_config(Dc::Map(Some(
                map_dc_str.to_string(),
            )))]),
        )?;
        let map = serde_json::from_str(map_dc_str).unwrap();
        let dc_res = d.get_map("map_dynamic_config".to_string(), &ctx);
        match dc_res {
            Ok(res) => {
                if res == map {
                    println!("got expected map: {:#?}", res)
                } else {
                    panic!()
                }
            }
            _ => panic!(),
        }

        Ok(())
    }

    #[test]
    fn get_map_errors_on_missing_name() -> Result<(), DeciderInitError> {
        let ctx = make_ctx(None)?;
        let d = build_decider(
            Some("darkmode fractional_availability value".to_string()),
            None,
            None,
        )?;
        let r = d.get_map("missing".to_string(), &ctx);
        match r {
            Ok(_) => panic!(),
            Err(e) => println!("got expected error: {:#?}", e),
        }
        Ok(())
    }

    #[test]
    fn test_value_eq() -> Result<(), String> {
        let v = json!({
            "s": "a string",
            "s2": "a string",
            "sn": "7",
            "n": 7i64,
            "bt1": true,
            "bt2": true,
            "bf": false,
            "bf2": false,
            "a": ["1", "2"],
            "o": {"a": 7i64}});

        // these comparisons are sensible enough...
        assert!(value_eq(&v["n"].clone(), &v["n"].clone()).unwrap());
        assert!(value_eq(&v["s"].clone(), &v["s"].clone()).unwrap());
        assert!(value_eq(&v["s"].clone(), &v["s2"].clone()).unwrap());
        assert!(value_eq(&v["bf"].clone(), &v["bf2"].clone()).unwrap());
        assert!(value_eq(&v["sn"].clone(), &v["n"].clone()).unwrap());
        assert!(value_eq(&v["n"].clone(), &v["sn"].clone()).unwrap());
        assert!(value_eq(&v["bt1"].clone(), &v["bt2"].clone()).unwrap());

        // ...if sometimes false...
        assert!(!value_eq(&v["sn"].clone(), &v["s2"].clone()).unwrap());
        assert!(!value_eq(&v["n"].clone(), &v["s"].clone()).unwrap());
        assert!(!value_eq(&v["bt"].clone(), &v["bf"].clone()).unwrap());

        // but here lies madness
        assert!(value_eq(&v["n"].clone(), &v["tb"].clone()).is_err());
        assert!(value_eq(&v["n"].clone(), &v["a"].clone()).is_err());
        assert!(value_eq(&v["a"].clone(), &v["o"].clone()).is_err());
        assert!(value_eq(&v["a"].clone(), &v["a"].clone()).is_err());
        Ok(())
    }
}
