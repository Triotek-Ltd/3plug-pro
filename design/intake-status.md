# 3plug Intake Status

## Status

Current public and community intake is complete for this pass.

This does **not** mean every business vertical has a strong mature shared app.

It means:

* we have done a broad best-effort intake sweep
* we have internalized the strongest public bases we found
* the remaining gaps are mostly broader product layers, not obviously missed public apps

## Internalized bases now in place

### Strong shared bases

* `triotek-lending`
* `triotek-education`
* `triotek-lms`
* `triotek-webshop`
* `triotek-posawesome`
* `triotek-healthcare`
* `triotek-utility-billing`
* `triotek-agriculture`

### Archived or reference-first bases

* `triotek-non-profit`
* `triotek-hospitality-base`
* `triotek-property-management-base`
* `triotek-logistics-base`
* `triotek-construction-base`
* `triotek-telecom-base`
* `triotek-livestock-base`
* `triotek-services-base`
* `triotek-aviation-base`
* `triotek-manufacturing-base`
* `triotek-restaurant-base`
* `triotek-vehicle-trading-base`
* `triotek-public-procurement-base`

## What remains intentionally native

This pass leaves `triotek-trading-base` as the clearest retained native functional layer from the deleted placeholder set.

## Important interpretation

Some of the remaining native layers are native because:

* the public references are too narrow
* the public references are archived
* the public references are niche or implementation-specific
* the broader product layer still belongs to Triotek

Example:

* `triotek-trading-base` is broader than `triotek-vehicle-trading-base`

## Operational conclusion

Intake should now pause.

The next phase should be:

1. normalize any remaining local naming cleanup
2. use the Frappe framework to turn `triotek-trading-base` into the intentional retained product layer
3. start real work there instead of continuing endless repo hunting
