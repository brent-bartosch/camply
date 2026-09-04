# Coveted Campsites Within a Few Hours of Los Angeles

**Purpose:** Reference file for an automated reservation agent (e.g. driven by [Camply](https://github.com/juftin/camply)). Each entry lists the booking provider, the booking-window behavior, and a recommended trigger strategy so the agent can decide between *opening-window sniping* and *continuous cancellation watching*.

**Home base:** Los Angeles, CA
**User preferences:** coastal sites, views, water, and high-privacy / low-occupancy grounds.
**Explicit exclusions:** No island sites and nothing requiring a ferry or boat to access (Channel Islands excluded by request).

---

## How to read the booking metadata

- **provider** — Which reservation system holds the inventory. Determines the Camply provider flag.
  - `RecreationGov` → Camply default provider.
  - `ReserveCalifornia` → Camply `--provider ReserveCalifornia`.
- **booking_window** — When inventory is released.
  - `rolling_6mo_daily_8am_PT` → ReserveCalifornia releases a new day 6 months out, every day, at 08:00 Pacific. Poll the specific target date 6 months ahead rather than waiting for one annual drop.
  - `rolling_6mo` (RecreationGov) → typically a 6-month rolling window; confirm per-campground as some NPS sites differ.
- **trigger_strategy** — Recommended automation mode.
  - `snipe_opening` → Inventory sells out in minutes; be polling exactly when the window opens.
  - `continuous_watch` → Inventory churns via cancellations; run an always-on search.
  - `both` → Snipe at open, then leave a continuous watcher running for cancellations.
- **ids_needed** — IDs the agent must resolve before running (use `camply campgrounds --search "<name>"` to discover, then confirm).

---

## Tier 1 — White whales (snipe the opening window)

### Julia Pfeiffer Burns Environmental Sites (Big Sur)
```yaml
name: Julia Pfeiffer Burns Environmental Campsites
region: Big Sur / Central Coast
drive_from_la: ~5-6 hours
provider: ReserveCalifornia
booking_window: rolling_6mo_daily_8am_PT
trigger_strategy: snipe_opening
matches_preferences: [view, water, privacy, coastal]
ids_needed: [park_id, campground_id]
notes: >
  Only two walk-in environmental sites in the entire park; among the hardest
  to book in California, sells out within minutes of release. Site #1 is at the
  cliff edge with full ocean panorama; site #2 is more sheltered with a redwood
  backdrop. NO WATER on site — nearest spigot ~0.5 mi away at parking lot.
  Weekdays meaningfully easier than weekends.
```

### Crystal Cove State Park (Orange County)
```yaml
name: Crystal Cove State Park
region: Orange County coast
drive_from_la: ~1-1.5 hours
provider: ReserveCalifornia
booking_window: rolling_6mo_daily_8am_PT
trigger_strategy: both
matches_preferences: [view, water, coastal]
ids_needed: [park_id, campground_id]
notes: >
  Beachfront. Moro campground sites and the historic cottages are notoriously
  hard to get. SoCal-coastal version of the dream without the Big Sur drive.
```

---

## Tier 2 — Coastal (extends Leo Carrillo / Malibu Creek)

### Point Mugu State Park — Thornhill Broome Beach
```yaml
name: Point Mugu State Park (Thornhill Broome)
region: Ventura County coast
drive_from_la: ~1 hour
provider: ReserveCalifornia
booking_window: rolling_6mo_daily_8am_PT
trigger_strategy: continuous_watch
matches_preferences: [view, water, coastal]
ids_needed: [park_id, campground_id]
notes: >
  Camp right on the sand, just up the coast from Leo Carrillo. Ocean plus
  mountains in one stay.
```

### El Capitán & Refugio State Beaches (Santa Barbara)
```yaml
name: El Capitan / Refugio State Beaches
region: Santa Barbara coast
drive_from_la: ~2-2.5 hours
provider: ReserveCalifornia
booking_window: rolling_6mo_daily_8am_PT
trigger_strategy: both
matches_preferences: [view, water, coastal]
ids_needed: [park_id, campground_id]   # two separate parks; resolve each
notes: >
  Palm-lined beachfront. Fills instantly in summer. Treat as two distinct
  targets.
```

---

## Tier 3 — Mountain / forest (cooler, Sierra-like escapes)

### Buckhorn Campground (San Gabriel Mountains)
```yaml
name: Buckhorn Campground
region: Angeles National Forest / San Gabriel Mtns
drive_from_la: ~50 miles (~1.5 hours)
provider: RecreationGov
booking_window: rolling_6mo
trigger_strategy: continuous_watch
matches_preferences: [view, forest, privacy]
ids_needed: [recreation_area_id, campground_id]
notes: >
  Woodsy San Gabriels site that feels like the Sierra Nevada. Local sleeper.
```

### Big Bear Area (San Bernardino Mountains)
```yaml
name: Big Bear area campgrounds (e.g. Serrano, Pineknot)
region: San Bernardino National Forest
drive_from_la: ~2-2.5 hours
provider: RecreationGov
booking_window: rolling_6mo
trigger_strategy: both
matches_preferences: [view, water, forest]
ids_needed: [recreation_area_id, campground_id]
notes: >
  Most versatile mountain getaway near LA; forest plus lake plus snow seasons.
  Serrano is the lakeside option. Some private/glamping inventory sits outside
  RecreationGov.
```

### Idyllwild (San Jacinto Mountains)
```yaml
name: Idyllwild campgrounds
region: San Jacinto Mountains
drive_from_la: ~2.5 hours
provider: mixed   # state park sites = ReserveCalifornia; USFS sites = RecreationGov
booking_window: rolling_6mo / rolling_6mo_daily_8am_PT
trigger_strategy: continuous_watch
matches_preferences: [view, forest, privacy]
ids_needed: [park_id_or_recreation_area_id, campground_id]
notes: >
  Quietest of the close mountain options. Confirm whether the specific
  campground is state park (ReserveCalifornia) or Forest Service (RecreationGov)
  before configuring.
```

---

## Tier 4 — Desert (stargazing, dramatic landscapes)

### Joshua Tree National Park
```yaml
name: Joshua Tree NP campgrounds (Jumbo Rocks, Indian Cove, Ryan, Black Rock)
region: High desert
drive_from_la: ~2.5-3 hours
provider: RecreationGov
booking_window: rolling_6mo
trigger_strategy: continuous_watch   # heavy cancellation churn; also snipe in peak
matches_preferences: [view, stargazing, dramatic]
ids_needed: [recreation_area_id, campground_id]   # per campground
notes: >
  Demand wildly outstrips supply in spring/fall. Strong continuous-watch target
  because of constant cancellations. Jumbo Rocks and Indian Cove are the
  scenic standouts.
```

### Saddleback Butte State Park (Mojave)
```yaml
name: Saddleback Butte State Park
region: Mojave Desert (Antelope Valley)
drive_from_la: ~1.5 hours
provider: ReserveCalifornia
booking_window: rolling_6mo_daily_8am_PT
trigger_strategy: continuous_watch
matches_preferences: [stargazing, privacy, solitude]
ids_needed: [park_id, campground_id]
notes: >
  Lesser-known. Quiet desert tent camping; strong "ground to ourselves" pick
  with dark night skies.
```

### Anza-Borrego Desert State Park
```yaml
name: Anza-Borrego Desert State Park (developed campgrounds)
region: Colorado Desert
drive_from_la: ~3 hours
provider: ReserveCalifornia
booking_window: rolling_6mo_daily_8am_PT
trigger_strategy: continuous_watch
matches_preferences: [stargazing, privacy, dramatic]
ids_needed: [park_id, campground_id]
notes: >
  Developed campgrounds (e.g. Borrego Palm Canyon) are reservable; much of the
  park is free dispersed camping needing no booking. Spring wildflower season
  spikes demand.
```

---

## Provider summary (for config grouping)

| Provider | Sites |
|---|---|
| RecreationGov (Camply default) | Buckhorn, Big Bear, Joshua Tree, Idyllwild (USFS sites) |
| ReserveCalifornia (`--provider ReserveCalifornia`) | Julia Pfeiffer Burns, Crystal Cove, Point Mugu, El Capitan, Refugio, Saddleback Butte, Anza-Borrego, Idyllwild (state-park sites) |

## Agent operating notes

1. **Resolve IDs first.** Every entry needs recreation-area/park and campground IDs resolved via `camply campgrounds --search "<name>"` before any search runs. Do not hardcode from memory.
2. **Verify provider/flags at runtime.** Camply's provider names and flags shift between releases; confirm the current `ReserveCalifornia` provider string and available options before relying on them.
3. **ReserveCalifornia window logic.** Use rolling daily polling for a target date 6 months out at 08:00 PT, not a single annual drop.
4. **Match strategy to mode.** `snipe_opening` for Tier 1; `continuous_watch` for cancellation-heavy sites (Joshua Tree, Point Mugu, Saddleback Butte); `both` where opening-day and churn both matter.
5. **Notifications.** Wire a notification provider (Pushover / email / Telegram) so secured matches surface immediately.