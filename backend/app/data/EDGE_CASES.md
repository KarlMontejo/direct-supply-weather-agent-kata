# Edge Cases & Test Scenarios

This document explains the intentional design decisions in the mock datasets
and what procurement scenarios each data point is built to challenge.

**All contracts and compliance rules apply exclusively to Karl's Senior Living of Dallas.**

---

## Facility

| Facility | Description |
|---|---|
| `karls_senior_living_dallas` | Karl's Senior Living of Dallas — the only facility in the system. All contracts apply to this facility alone. Users are procurement agents for Karl's Senior Living of Dallas requesting assistance with their procurement workflows. |

---

## Edge Case Matrix

### 1. Compliant Product is Out of Stock → Forces Substitution

- **Product #5** (Chicken Breast, Prime Poultry, 5 lb) — fully contract-compliant for Karl's Senior Living of Dallas
- **Inventory**: OUT OF STOCK at `southeast_dc`, available at midwest/northeast
- **Challenge**: Agent must detect the stock-out, check other DCs, or find a compliant substitute
- **Trap**: Product #38 (Budget Chicken Breast, ValueMeats) is identical, cheaper ($12.99 vs $18.99), available everywhere — but **off-contract** (ValueMeats is not an approved supplier for Karl's Senior Living of Dallas)

### 2. Off-Contract Brand Looks Attractive (Cost vs Compliance)

- **Product #38** (Budget Chicken Breast, ValueMeats, $12.99) — same 5 lb chicken, $6 cheaper
- **Product #5** (Prime Poultry, $18.99) — on contract for Karl's Senior Living of Dallas
- **Challenge**: Agent must prefer the compliant option and explain the cost difference, not just pick the cheapest

### 3. Expired Contract (Pasta)

- **Contract #5** (Bella Italia pasta) — **EXPIRED** on 2025-12-31 (`is_active = 0`)
- **Contract #6** (Heritage Pasta) — current replacement, effective 2026-01-01
- **Product #7** (Spaghetti, Bella Italia, $1.89) — in stock everywhere, cheap, but contract expired for Karl's Senior Living of Dallas
- **Product #44** (Spaghetti Heritage, $2.29) — compliant under new contract, but LOW STOCK at midwest and OUT at southeast/northeast
- **Challenge**: Agent must recognize the expired contract and recommend Heritage Pasta despite availability issues. Forces a tough tradeoff: compliant but scarce vs available but non-compliant.

### 4. Prohibited Ingredients — Peanuts at Karl's Senior Living of Dallas

- **Product #12** (Peanut Butter, NutHouse) — off-contract for Karl's; peanuts prohibited
- **Contract #8** (Pantry — Karl's Senior Living of Dallas) — **prohibits peanuts and tree nuts**, removes NutHouse from approved brands
- **Product #35** (Sunflower Seed Butter, SunSpread) — nut-free alternative, compliant for Karl's
- **Inventory**: Sunflower Seed Butter is LOW STOCK at all DCs (3-5 units)
- **Challenge**: Agent must reject peanut butter and recommend the nut-free substitute despite limited availability.

### 5. Prohibited Ingredients — Pork/Shellfish at Karl's Senior Living of Dallas

- **Product #39** (Pork Sausage, Midwest Meats) — pork prohibited per Karl's contracts
- **Contract #13** (Breakfast — Karl's Senior Living of Dallas) — **prohibits pork**, removes Midwest Meats
- **Product #40** (Turkey Sausage, Prime Poultry) — compliant for Karl's
- **Product #37** (Frozen Shrimp, OceanCatch) — brand is on protein contract, but **shrimp = shellfish** → prohibited per Karl's Contract #2
- **Challenge**: Brand approval alone isn't enough. The agent must also check the prohibited_ingredients list against the product's actual ingredients.

### 6. Sodium Limit — Prepared Meals at Karl's Senior Living of Dallas

- **Product #27** (Chicken Noodle Soup, 890mg sodium) — **FAILS** Karl's contract (max 600mg, requires low_sodium flag)
- **Product #36** (Low Sodium Chicken Noodle Soup, 380mg, has low_sodium flag) — compliant for Karl's
- **Inventory**: Low Sodium Soup is OUT at `southeast_dc`
- **Challenge**: Agent must recommend #36 over #27 and flag the southeast stock-out.

### 7. Partial Stock-Out → Quantity Adjustment

- **Product #10** (Cheddar Cheese, DairyCraft) — only **3 units** at `midwest_dc` (low_stock)
- Southeast and northeast have 25+ units
- **Challenge**: If someone orders 20 units from midwest, agent must flag that only 3 are available and suggest sourcing from another DC or reducing quantity.

### 8. Hard Stock-Out Across All DCs

- **Product #33** (Brown Rice 20 lb, Heartland) — **0 units at ALL distribution centers**
- **Product #26** (Brown Rice 10 lb, Heartland) — available, compliant for Karl's, but smaller pack size
- **Challenge**: Agent must detect the total stock-out and suggest the 10 lb alternative, noting the pack size difference and potential cost-per-unit impact.

### 9. Regional Availability Gap

- **Product #9** (Frozen Broccoli, GreenFields) — OUT at `southeast_dc`, available at midwest/northeast
- **Product #25** (Frozen Mixed Veg, GreenFields) — available everywhere, same category
- **Challenge**: Agent must check DC-specific inventory and suggest alternatives or cross-DC sourcing for southeast orders.

### 10. Off-Contract Dairy (Brand Mismatch)

- **Product #22** (Pizza Cheese Blend, Bella Italia) — brand "Bella Italia" is a pasta brand, NOT in the dairy contract's approved brands for Karl's Senior Living of Dallas
- **Contract #3** (Dairy) approves: DairyPure, DairyCraft, Cultured Dairy, Sunny Farm
- **Challenge**: Product exists in the dairy category but its brand isn't on the dairy contract. Agent must flag the compliance issue.

### 11. Off-Contract Bread (Cheap but Non-Compliant)

- **Product #34** (White Bread, BudgetBake, $1.99) — cheap but BudgetBake is NOT in the grains_bread contract for Karl's Senior Living of Dallas
- **Product #1** (Whole Wheat Bread, Golden Grain, $3.49) — compliant for Karl's
- **Challenge**: Similar to the chicken breast scenario — agent must choose compliance over price.

### 12. Frozen Lasagna — Regional + Compliance Trap

- **Product #42** (Frozen Lasagna, Bella Italia, 820mg sodium) — only available at `midwest_dc`
- **FAILS** Karl's Senior Living of Dallas contracts: max 600mg sodium, requires low_sodium flag, HomeStyle brand only for prepared meals
- **Challenge**: Multiple simultaneous violations. Agent must identify all of them.

---

## Summary of Compliance Outcomes for Karl's Senior Living of Dallas

| Product | Compliant? | Why |
|---|---|---|
| #5 Chicken Breast (Prime Poultry) | ✅ | On contract |
| #7 Spaghetti (Bella Italia) | ❌ | Contract expired |
| #12 Peanut Butter (NutHouse) | ❌ | Peanuts prohibited |
| #22 Pizza Cheese (Bella Italia) | ❌ | Brand not on dairy contract |
| #27 Chicken Soup (890mg) | ❌ | Exceeds sodium + missing low_sodium flag |
| #32 Breaded Chicken (CrispyBird) | ❌ | Brand not on protein contract |
| #34 White Bread (BudgetBake) | ❌ | Brand not on grains contract |
| #37 Shrimp (OceanCatch) | ❌ | Shellfish prohibited |
| #38 Budget Chicken (ValueMeats) | ❌ | Supplier not on contract |
| #39 Pork Sausage (Midwest Meats) | ❌ | Pork prohibited |
| #42 Frozen Lasagna (Bella Italia) | ❌ | Brand + sodium + dietary flag violations |
| #44 Heritage Spaghetti | ✅ | On current pasta contract |
