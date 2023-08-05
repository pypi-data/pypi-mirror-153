use fst::Automaton;
use std::cmp;


#[derive(Clone)]
pub(crate) struct DynamicLevenshtein {
    query: String,
    dist: usize,
}

impl DynamicLevenshtein {
    pub fn new(query: impl Into<String>, dist: usize) -> Self {
        Self{query: query.into(), dist}
    }
}

impl DynamicLevenshtein {
    fn start(&self) -> Vec<usize> {
        (0..self.query.chars().count() + 1).collect()
    }

    fn is_match(&self, state: &[usize]) -> bool {
        state.last().map(|&n| n <= self.dist).unwrap_or(false)
    }

    fn can_match(&self, state: &[usize]) -> bool {
        state.iter().min().map(|&n| n <= self.dist).unwrap_or(false)
    }

    fn accept(&self, state: &[usize], chr: Option<char>) -> Vec<usize> {
        let mut next = vec![state[0] + 1];
        for (i, c) in self.query.chars().enumerate() {
            let cost = if Some(c) == chr { 0 } else { 1 };
            let v = cmp::min(
                cmp::min(next[i] + 1, state[i + 1] + 1),
                state[i] + cost,
            );
            next.push(cmp::min(v, self.dist + 1));
        }
        next
    }
}


#[derive(Clone, Debug)]
pub(crate) struct DynamicLevenshteinUtf8State {
    lev: Vec<usize>,
    bytes: Vec<u8>,
}

impl Automaton for DynamicLevenshtein {
    type State = DynamicLevenshteinUtf8State;

    fn start(&self) -> Self::State {
        DynamicLevenshteinUtf8State{
            lev: self.start(),
            bytes: Vec::with_capacity(4),
        }
    }

    fn accept(&self, state: &Self::State, byte: u8) -> Self::State {
        let mut new_state = state.clone();
        new_state.bytes.push(byte);
        let char = std::str::from_utf8(&new_state.bytes)
            .ok()
            .and_then(|s| s.chars().next());
        if let Some(char) = char {
            new_state.bytes.clear();
            new_state.lev = self.accept(&new_state.lev, Some(char));
        }
        new_state
    }

    fn is_match(&self, state: &Self::State) -> bool {
        self.is_match(&state.lev) && state.bytes.is_empty()
    }

    fn can_match(&self, _state: &Self::State) -> bool {
        self.can_match(&_state.lev)
    }
}
