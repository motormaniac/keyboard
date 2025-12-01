use std::collections::{HashMap, btree_map::Values};

mod fileio;

fn main() {
    let data_map = fileio::read_data("data/combination_key_data.txt", HashMap::new());
    let mut keys:Vec<&String> = Vec::new();
    for (key, submap) in data_map.iter() {
        keys.push(key);
        for (subkey, _) in submap.iter() {
            keys.push(subkey)
        }
    }
    println!("{keys:?}");
}
