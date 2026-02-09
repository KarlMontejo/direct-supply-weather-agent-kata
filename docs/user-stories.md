# User Stories

## User Story 1: Hard Stock-Out Resolution

### User
> “The pre-cooked turkey sausage we usually order is unavailable. What should I order instead?”

### Agent Behavior
- Detects stock-out intent  
- Confirms unavailability via Inventory API  
- Retrieves compliance rules via Contracts API  
- Searches for candidate alternatives via Product Search  
- Uses Open Food Facts to validate ingredient equivalence  
- Filters for availability and compliance  

### Agent Response
> “The requested turkey sausage is currently unavailable. A compliant alternative is Brand B pre-cooked turkey sausage, which is available and meets your contract requirements. It matches the same protein source and dietary constraints, with a slightly different seasoning profile.”

---

## User Story 2: Partial Stock-Out with Order Revision

### User
> “We need 10 cases of this product, but I heard availability is limited.”

### Agent Behavior
- Confirms partial availability (e.g., 4 cases available)  
- Suggests partial fulfillment  
- Recommends substitute for remaining quantity  

### Agent Response
> “Only 4 of the 10 requested cases are currently available. I recommend ordering the available quantity and substituting the remaining 6 cases with Brand C, which is contract-compliant and in stock.”

---

## User Story 3: Contract Compliance Check

### User
> “Is this product compliant with our contract?”

### Agent Behavior
- Inspects product details  
- Cross-validates brand, pack size, supplier, and effective dates  

### Agent Response
> “This product is not contract-compliant due to an unapproved pack size. The 10 lb case of the same product is approved under your current agreement.”

---

## User Story 4: Curated Product Search

### User
> “Show me compliant chicken breast options we can order right now.”

### Agent Behavior
- Queries contract-approved product list  
- Filters by current inventory availability  
- Ranks options by relevance  

### Agent Response
> “Here are three contract-compliant chicken breast products currently available. Option A is the closest match to your standard order, while Option B offers a lower price per unit.”

---

## User Story 5: Requirement Cross-Validation

### User
> “We need a substitute that meets low-sodium dietary requirements.”

### Agent Behavior
- Retrieves dietary constraints from contract data  
- Uses Open Food Facts to compare nutrition data  
- Eliminates non-compliant products  

### Agent Response
> “Brand D meets the low-sodium requirement and is the closest ingredient match. Brand E exceeds sodium limits and is not recommended.”

---

## User Story 6: Drafting an Order Recommendation

### User
> “Can you help me revise today’s order based on what’s available?”

### Agent Behavior
- Reviews existing order  
- Flags unavailable or risky items  
- Suggests substitutions  
- Produces a draft order summary  

### Agent Response
> “Based on current availability, I recommend the following changes to today’s order… This draft preserves compliance and avoids stock-outs.”