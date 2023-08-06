use pyo3::prelude::*;

use crate::item::ItemStruct;
use crate::primitive::PrimitiveItem;

#[derive(Debug, Clone)]
#[pyclass]
pub struct MapItem {
    #[pyo3(get)]
    prefix: String,
    #[pyo3(get)]
    values: Vec<(PrimitiveItem, ItemStruct)>,
}


impl MapItem {
    pub fn new(prefix: String) -> Self {
        Self {
            prefix,
            values: vec![],
        }
    }

    pub fn insert(&mut self, k: PrimitiveItem, v: ItemStruct) {
        self.values.push((k, v.clone()));
    }
}