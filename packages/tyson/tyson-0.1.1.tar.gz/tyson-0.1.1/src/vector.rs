use pyo3::prelude::*;

use crate::item::ItemStruct;

#[derive(Debug, Clone)]
#[pyclass]
pub struct VectorItem {
    #[pyo3(get)]
    prefix: String,
    #[pyo3(get)]
    items: Vec<ItemStruct>,
}


impl VectorItem {
    pub fn new(prefix: String) -> Self {
        Self {
            prefix,
            items: vec![],
        }
    }

    pub fn push(&mut self, item: ItemStruct) {
        self.items.push(item);
    }
}
