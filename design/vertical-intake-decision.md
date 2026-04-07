# 3plug Vertical Intake Decision

## Purpose

This is the working decision layer for vertical repo strategy.

It answers one operational question:

Which verticals should Triotek intake from an existing public Frappe codebase, which ones should be reference-only, and which ones should stay native-first?

This decision is based on [vertical-availability-map.md](vertical-availability-map.md).

## Intake now

These have a strong enough public base that we should keep them in the governed source ecosystem as upstream-derived repos.

| Vertical | Triotek repo | Public base | Decision |
| --- | --- | --- | --- |
| Finance / lending | `triotek-lending` | `frappe/lending` | Intake now |
| Education | `triotek-education` | `frappe/education` | Intake now |
| LMS / training | `triotek-lms` | `frappe/lms` | Intake now |
| Commerce | `triotek-webshop` | `frappe/webshop` | Intake now |
| Retail POS | `triotek-posawesome` | `ucraft-com/POS-Awesome` | Intake now |
| Healthcare | `triotek-healthcare` | `ESS-LLP/healthcare` | Intake now |
| Utility billing | `triotek-utility-billing` | `navariltd/utility-billing` | Intake now |
| Agriculture | `triotek-agriculture` | `frappe/agriculture` | Intake now, but review version fit during adoption |
| Nonprofit / NGO | `triotek-non-profit` | `frappe/non_profit` | Intake now as a reference-first archived base |
| Hospitality | `triotek-hospitality-base` | `frappe/hospitality` | Intake now as a reference-first archived base |
| Property management | `triotek-property-management-base` | `aakvatech/PropMS` | Intake now as a reference-first community base |
| Logistics | `triotek-logistics-base` | `hrgadeha/logistics` | Intake now as a reference-first community base |
| Construction | `triotek-construction-base` | `aidgoc/fibertrack-pro` | Intake now as a reference-first community base |
| Telecom | `triotek-telecom-base` | `macrobian88/frappe_zain_subscriptions` | Intake now as a reference-first community base |
| Livestock | `triotek-livestock-base` | `Janviere-dev/Livestock_Management` | Intake now as a reference-first community base |
| Services | `triotek-services-base` | `j4ptl/FSM-field_service_management` | Intake now as a reference-first community base |
| Aviation | `triotek-aviation-base` | `RohanRks23/airplane_mode` | Intake now as a reference-first community base |
| Manufacturing | `triotek-manufacturing-base` | `efeone/aumms` | Intake now as a reference-first community base |
| Restaurant / food service | `triotek-restaurant-base` | `alialiens/erpnext_restaurant` | Intake now as a reference-first community base |
| Vehicle trading | `triotek-vehicle-trading-base` | `AddonSolutionsForERPnext/Custom_Car_Trading_App` | Intake now as a reference-first community base |
| Public procurement | `triotek-public-procurement-base` | `buff0k/procurement` | Intake now as a reference-first community base |

## Intake carefully

These have a real public codebase, but they carry maintenance risk, archival risk, or naming ambiguity. They should not be treated like clean current upstreams without review.

At the moment, there are no remaining verticals in this bucket that we have chosen to intake immediately.

## Reference-first community and niche bases

These have community or niche public repos we should not ignore, but they are not yet strong enough to treat like clean shared upstreams without review.

| Vertical | Triotek repo | Decision |
| --- | --- | --- |
| Trading / distribution | `triotek-trading-base` | General trading still depends more on ERPNext plus niche references than on one strong shared public app |

## Immediate next moves

1. Keep all current vertical base repos where they are under `apps-vertical`.
2. Treat `triotek-non-profit` as the single NGO/non-profit repo unless a later split becomes justified.
3. Treat `triotek-property-management-base`, `triotek-logistics-base`, `triotek-construction-base`, `triotek-telecom-base`, and `triotek-livestock-base` as reference-first bases for now, and only create separate product layers later if the split becomes justified.
4. Treat `triotek-healthcare` as the single healthcare repo for now instead of splitting it into `triotek-healthcare` and `triotek-health`.
5. Start the first real native vertical work in `triotek-trading-base`.
6. Treat `triotek-manufacturing-base`, `triotek-restaurant-base`, and `triotek-vehicle-trading-base` as the public head starts for those narrower verticals, and only create separate broader product layers later if the split becomes justified.
7. Treat `triotek-public-procurement-base` as the public-sector procurement head start for current public-sector intake work.
8. Keep `triotek-trading-base` as the broader trading and distribution layer above the narrower `triotek-vehicle-trading-base`.
