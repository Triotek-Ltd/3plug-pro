# 3plug Vertical Availability Map

## Purpose

This note maps each Triotek vertical app to the closest public Frappe codebase we can actually verify.

The point is to separate:

* `Strong base exists`
* `Usable but weak / archived base exists`
* `No solid standalone app found`

That way we do not pretend every vertical already has a reusable app when some of them are really ERPNext-plus-custom work.

## Verdict

We do **not** have a strong public standalone codebase for all verticals.

We **do** have good public bases for a meaningful subset:

* agriculture
* nonprofit / NGO
* hospitality
* healthcare
* lending / finserv
* education
* LMS
* webshop / commerce
* retail POS
* utility billing
* property management / real estate references
* logistics references
* construction references
* telecom references
* services references
* manufacturing references
* livestock references
* aviation references

For the rest, the honest base is usually:

* `triotek-erpnext`
* plus a vertical Triotek app
* plus shared Triotek apps like `triotek-ke`, `triotek-payments`, `triotek-recon`, and `triotek-forensics`

## Vertical map

| Triotek vertical | Closest public base | Availability | Recommendation |
| --- | --- | --- | --- |
| `triotek-agriculture` | `frappe/agriculture` | Strong public base exists | Internalize the agriculture app and use it directly until a separate Triotek agribusiness layer is actually needed. |
| `triotek-non-profit` | `frappe/non_profit` | Public base exists, but archived | Use this as the single NGO/non-profit base for now. Keep it reference-first because the upstream is archived, and only split later if a real Triotek NGO product layer becomes necessary. |
| `triotek-healthcare` | `ESS-LLP/healthcare` | Strong community base exists | Use this as the single healthcare base and product repo for now. Do not keep a second duplicate `triotek-health` repo unless a later split becomes necessary. |
| `triotek-hospitality-base` | `frappe/hospitality` | Public base exists, but archived | Use this as the single hospitality base for now. Keep it reference-first because the upstream is archived, and only split later if a real Triotek hospitality product layer becomes necessary. |
| `triotek-livestock-base` | `diniemasjuki/erpnext_agro`, `Janviere-dev/Livestock_Management` | Community references exist | Use this as the single livestock reference base for now. Keep it reference-first because the available repos look niche and agriculture-adjacent rather than like a mature shared upstream. |
| `triotek-construction-base` | `aidgoc/fibertrack-pro`, `byoosi2022/Construction-Custom-Frappe` | Community references exist | Use this as the single construction reference base for now. Keep it reference-first because the available repos appear niche or implementation-specific rather than like a broad mature vertical base. |
| `triotek-logistics-base` | `hrgadeha/logistics`, `Neoadmin23/ascra_logistics`, `AnyGridTech/frappe_brazil_logistics` | Community references exist | Use this as the single logistics reference base for now. Keep it reference-first because the community repos are useful but still need Triotek shaping for real delivery. |
| `triotek-public-procurement-base` | `buff0k/procurement`, with weaker alternatives like `Halmontaser/tender` and `Dhruvang-cyg/gem` | Community procurement references exist | Use this as the strongest public-sector procurement head start we found. It has a real procurement module and meaningful doctypes such as purchase requisitions, supplier compliance, site allocation, and quotation attachments, while the tender and GEM candidates were noticeably thinner. |
| `triotek-manufacturing-base` | `efeone/aumms`, plus ERPNext manufacturing and `promantia-ltd/erpnext_manufacturing_app` | Built-in base plus community extensions exist | Use `triotek-manufacturing-base` as the public head start. It is meaningfully different from ERPNext manufacturing because it adds jewellery and process-specific doctypes, metal ledger flows, stage templates, design requests, and domain settings on top of the core manufacturing stack. |
| `triotek-services-base` | `j4ptl/FSM-field_service_management`, with `itgostack-ux/gofix` as a narrower repair-service alternative | Community references exist | Use this as the single services reference base for now. We selected the field-service candidate because it has real service, technician, visit-log, and SLA doctypes, while weaker candidates were too thin. Keep it reference-first because the available repos are still niche enough that Triotek should own the product layer later if needed. |
| `triotek-telecom-base` | `macrobian88/frappe_zain_subscriptions`, `khatrijitendra/telecom-frappe_v7`, `cholthi/crbt_mis` | Community references exist | Use this as the single telecom reference base for now. Keep it reference-first because there are real telecom-adjacent repos, though quality and freshness vary. |
| `triotek-aviation-base` | `RohanRks23/airplane_mode`, `younis-ali/airport-automation`, and similar flight / airport management repos | Community references exist | Use this as the single aviation reference base for now. Keep it reference-first because the repos found look niche, student-grade, or implementation-specific rather than like a mature shared base. |
| `triotek-vehicle-trading-base` | `AddonSolutionsForERPnext/Custom_Car_Trading_App`, plus ERPNext trading / distribution and `resilient-tech/ntc` | Built-in base plus niche community references | Use this as a vehicle-dealership reference base only. It is narrower than general trading/distribution, since the actual app modules and doctypes are car-specific (`Car Trading`, `Cars`, `car_brand`, `new_cars`, `old_cars`). |

## What this means for repo policy

### Internalize as true vertical bases

* `triotek-lending`
* `triotek-education`
* `triotek-lms`
* `triotek-webshop`
* `triotek-posawesome`
* `triotek-healthcare`
* `triotek-utility-billing`

### Intake now with review discipline

* `triotek-agriculture` from `frappe/agriculture`

### Reference-first archived bases now internalized

* `triotek-non-profit` from `frappe/non_profit`
* `triotek-hospitality-base` from `frappe/hospitality`

These should be treated carefully because:

* `non_profit` is archived
* `hospitality` is archived
* `agriculture` is now internalized, but still needs ongoing version-fit review against the major version strategy

### Reference-first community bases now internalized

* `triotek-property-management-base` from `aakvatech/PropMS`

This should be treated carefully because:

* it is a community base, not an official Frappe app
* real-estate delivery may still depend heavily on `triotek-utility-billing` and ERPNext

### Reference-first community and niche bases

* `triotek-livestock-base`
* `triotek-construction-base`
* `triotek-logistics-base`
* `triotek-manufacturing-base`
* `triotek-services-base`
* `triotek-telecom-base`
* `triotek-vehicle-trading-base`
* `triotek-aviation-base`
* `triotek-public-procurement-base`

### Keep native-first

## Recommended next repo moves

1. Keep `triotek-agriculture` as an internalized base under review for version-fit, without a duplicate `triotek-agri-ops` repo for now.
2. Keep `triotek-non-profit` as an internalized archived reference base, without a duplicate `triotek-ngo-ops` repo for now.
3. Keep `triotek-hospitality-base` as an internalized archived reference base, without a duplicate hospitality ops repo for now.
4. Keep `triotek-trading-base` as the retained broader trading and distribution layer above narrower niche trading references.
5. Treat `triotek-healthcare` as the single healthcare repo for now instead of splitting it prematurely into `healthcare` plus `health`.
6. Treat `triotek-public-procurement-base` as the current public-sector head start, without keeping a duplicate broader public-ops placeholder.

## Sources

* https://github.com/frappe/agriculture
* https://github.com/frappe/non_profit
* https://github.com/frappe/hospitality
* https://github.com/frappe/lending
* https://github.com/frappe/education
* https://github.com/frappe/lms
* https://github.com/frappe/webshop
* https://github.com/ESS-LLP/healthcare
* https://github.com/ucraft-com/POS-Awesome
* https://github.com/navariltd/utility-billing
* https://github.com/frappe/erpnext
* https://frappe.io/stories
* https://cloud.frappe.io/marketplace/apps/property_management
* https://discuss.frappe.io/t/property-management/21151
* https://github.com/aakvatech/PropMS
* https://github.com/hrgadeha/logistics
* https://github.com/Neoadmin23/ascra_logistics
* https://github.com/AnyGridTech/frappe_brazil_logistics
* https://github.com/aidgoc/fibertrack-pro
* https://github.com/byoosi2022/Construction-Custom-Frappe
* https://github.com/diniemasjuki/erpnext_agro
* https://github.com/Janviere-dev/Livestock_Management
* https://github.com/alialiens/erpnext_restaurant
* https://github.com/Rocket-Quack/erpnext_restaurant
* https://github.com/zubairamini/Restaurant-POS
* https://github.com/j4ptl/FSM-field_service_management
* https://github.com/itgostack-ux/gofix
* https://github.com/macrobian88/frappe_zain_subscriptions
* https://github.com/khatrijitendra/telecom-frappe_v7
* https://github.com/cholthi/crbt_mis
* https://github.com/aerele/apparelo
* https://github.com/efeone/aumms
* https://github.com/promantia-ltd/erpnext_manufacturing_app
* https://github.com/resilient-tech/ntc
* https://github.com/AddonSolutionsForERPnext/Custom_Car_Trading_App
* https://github.com/Dhruvang-cyg/gem
* https://github.com/buff0k/procurement
* https://github.com/michaelkaraz/ErpNext_V12_TenderMangement
* https://github.com/Halmontaser/tender
* https://github.com/MohamedAbdulsalam96/rft_cheques
* https://github.com/RohanRks23/airplane_mode
* https://github.com/nandinisevak03/Airplane-Ticket-Management
* https://github.com/younis-ali/airport-automation
* https://github.com/ayush2004patel/Frappe-Airport
