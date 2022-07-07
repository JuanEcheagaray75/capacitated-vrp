# TODO

## General

- [ ] Implement time window constraints
- [ ] Test app on Solomon VRP data
- [ ] Find another library for route visualization

## Visuals

- [ ] Design a proper dashboard
  - [ ] Define information to be included

## Report

- [x] Table of results
  - [x] Time of execution $\propto$ `search_parameters.time_limit.FromSeconds(t)`
    - [x] Better idea to create a graph that compares found optimal distance vs said time
  - [x] Wasted volume per vehicle
  - [x] Traveled distance per vehicle
  - [x] Load per vehicle
  - [x] Carbon footprint
  - [x] Table of results for justifying max execution time
    - [x] Calculate average
    - [x] Calculate variance
- [x] Properly define the study case
  - [x] Focus on the entire city
  - [x] Not using traffic
- [x] Update justification
  - [x] Talk about e-commerce and how logistics greatly influences the final cost of a product
- [x] Previous work <=> Theoretical framework
- [ ] Make a comparison of the previous work with our proposed framework
  - [ ] [VRP Spreadsheet solver 2020](https://www.sciencedirect.com/science/article/pii/S0305054817300552)
- [x] Define objectives
  - [x] General objectives
  - [x] Detailed objectives
- [x] Establish an hypothesis (null vs alternative)
- [x] Do not work on the infrastructure, not needed for our case
- [x] State resources used
  - [x] Computational resources
  - [x] Description of the generated network
- [ ] Results
  - [x] Map
  - [ ] Dashboard

### For the flex

- [ ] Planning (AI) for VRP
- [ ] Add an overall description of how to use our product