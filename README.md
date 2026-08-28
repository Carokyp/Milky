# Milky

<p align="center">
  <img src="docs/images/readme-preview.png" alt="Milky responsive preview" width="100%">
</p>

**Live Application:** https://milky-app-839f694f035d.herokuapp.com/

## About

**Milky** is a Django e-commerce website for a milkshake-in-a-can drinks brand. Visitors can browse the product range, read and leave reviews, add cans to a cart, check out with Stripe, and create an account to save delivery details and view past orders. A standout feature is **Gift a Can**: any logged-in customer can send a can straight to a friend's address as part of their order, and gets 10% off, without needing the friend's own account.

The site is deployed on Heroku, with static files and product images served from AWS S3 and transactional email sent over SMTP.

## Index – Table of Contents

* [User Experience (UX)](#user-experience-ux)
   * [Strategy](#strategy)
   * [User Stories](#user-stories)
   * [Scope](#scope)
   * [Structure](#structure)
   * [Skeleton](#skeleton)
   * [Wireframes](#wireframes)
   * [Surface](#surface)

* [Features](#features)

* [Error Pages](#error-pages)

* [Site Map](#site-map)

* [Technical Architecture](#technical-architecture)
   * [Admin Page](#admin-page)
   * [CRUD Operations](#crud-operations)
   * [User Feedback](#user-feedback)
   * [Database Schema](#database-schema)

* [Future Features](#future-features)

* [Technologies Used](#technologies-used)

* [Testing](#testing)
   * [Authentication](#authentication)
   * [CRUD](#crud)
   * [Permissions](#permissions)
   * [Forms](#forms)
   * [UX](#ux)
   * [Accessibility](#accessibility-1)
   * [Validator Testing](#validator-testing)
   * [Browser Compatibility](#browser-compatibility)
   * [Responsive Design](#responsive-design)
   * [Performance](#performance)
   * [Bugs Found, Fixed, and Unresolved](#bugs-found-fixed-and-unresolved)
   * [Testing User Stories](#testing-user-stories)

* [Security](#security)

* [Deployment](#deployment)
   * [Heroku](#heroku)
   * [Amazon Web Services (AWS)](#amazon-web-services-aws)
   * [Stripe](#stripe)
   * [Emails](#emails)
   * [Forking & Cloning the Repository](#forking--cloning-the-repository)

* [Credits](#credits)
   * [Visual Design References](#visual-design-references)
   * [Code References](#code-references)
   * [Media](#media)
   * [Acknowledgements](#acknowledgements)

## User Experience (UX)

### Strategy

With **Milky**, the goal was a warm, playful storefront for a single drinks brand that makes browsing flavors and checking out feel effortless, while giving the brand a low-friction way to turn customers into referrers through the Gift a Can feature.

#### Business goals of the website
- Present the product range attractively enough to drive purchases from a cold visit.
- Keep checkout friction low — guests can buy without an account, Stripe handles payment.
- Turn one-time buyers into repeat customers by saving delivery info and order history behind an account.
- Use Gift a Can as a built-in referral loop: a customer gets 10% off, a friend gets a free introduction to the brand.

#### Customer goals of the website
- Quickly understand what Milky is and see the available flavors.
- Get enough detail (description, nutrition facts, reviews) to decide before buying.
- Add products to a cart and check out quickly, with or without creating an account.
- Send a can as a gift to a friend in a couple of clicks.
- Manage delivery/invoice details and revisit past orders without re-entering everything.

#### Reasons for the website
- Direct-to-consumer sales channel for the Milky brand.
- Referral/gifting growth loop via Gift a Can.
- Building a returning customer base through saved profiles and order history.
- Collecting product reviews as social proof for new visitors.

### User Stories

**New Visitor**
- As a new visitor, I want to see the product range and understand the brand, so I can decide if it's for me.
- As a new visitor, I want to view a product's description, nutrition facts, and reviews, so I can make an informed choice.
- As a new visitor, I want to add products to my cart and check out as a guest, so I don't have to register just to buy something.
- As a new visitor, I want to create an account, so my delivery details are saved for next time.

**Existing User**
- As an existing user, I want to sign in and see my checkout form pre-filled with my saved details, so re-ordering is fast.
- As an existing user, I want to view my order history, so I can see what I've bought and when.
- As an existing user, I want to save a friend as a contact, so I can gift them a can without re-entering their details every time.
- As an existing user, I want to reset my password if I forget it.
- As an existing user, I want to leave a star rating and comment on a product, so I can share my opinion with other shoppers.

**All Users**
- As a user, I want clear confirmation before a destructive action (deleting a product, a saved contact) so I don't lose data by accident.
- As a user, I want feedback (toasts, inline form errors) after every action, so I always know whether it worked.
- As a user, I want the site to work well on my phone, tablet, and desktop.

### Scope

#### In scope Features:
- Product catalogue with a featured selection on the home page and a full grid on All Products.
- Product detail page: nutrition facts, benefit highlights, paginated reviews, and a review submission form for authenticated users.
- Session-based cart (add / update quantity / remove) with a live free-delivery progress banner, no account required.
- Gift a Can: pick a product and a recipient (saved contact or a new one), add an optional message, get 10% off the order.
- Stripe Payment Element checkout, with delivery + optional separate invoice address.
- Order confirmation page, reused as the order-detail view from the account's order history.
- Account system (django-allauth): register, sign in/out, mandatory email verification, password reset/change, email management.
- Profile page with three tabs: edit personal details, view order history, manage saved gift contacts (full CRUD).
- Superuser-only Products Management: add, edit, and delete products directly from the storefront UI.
- Toast notification system (success / error / warning / info) with a dynamic mini-cart preview on "added to cart" toasts.
- Custom branded 404 / 403 / 405 / 500 error pages.

#### Out of scope Features:
- Product search, filtering, or sorting.
- Wishlists or saved-for-later items.
- Subscriptions / recurring orders.
- Multiple gift recipients per order (currently limited to one gift per order).
- Editing or deleting an existing review once submitted.
- Self-service account deletion.
- Social login (Google/Facebook) — allauth is installed but no providers are configured.
- Real-time order tracking or shipping notifications.
- Loyalty points or a rewards program.
- Live chat support.

### Structure

The home page leads with a hero (an animated 3D can rendered with Three.js) and a "Shop Now" call to action, followed by a featured-products showcase and a nutrition/benefits section. From there, the flow is intentionally linear: browse products → view a product's detail page → add to cart → check out. A persistent navbar keeps Home, All Products, and Gift a Can within reach at all times, with the authenticated links (Profile, Products Management for superusers, Logout) appearing once signed in.

Milky is a multi-page application (MPA) with server-side rendering via Django — each route renders a dedicated template rather than switching views inside a single-page app. The cart and the in-progress gift selection both live in the session rather than the database, so nothing is written to the database until an order is actually placed.

Key sections and navigation flow:
- Home: hero with 3D can, featured products, nutrition/benefits section.
- All Products: full catalogue grid.
- Product Detail: description, nutrition facts, reviews, add to cart.
- Gift a Can: promo landing page for guests, full gift form for logged-in users.
- Cart: line items, gift line (if any), order summary.
- Checkout: delivery/invoice form + Stripe Payment Element.
- Order Confirmation: reused for both the post-checkout success page and the profile's order-history detail view.
- Auth: register, sign in, password reset, email verification (django-allauth).
- Profile: My Profile / Orders / Contacts tabs.
- Products Management (superuser only): add/edit/delete products.

#### Technical Implementation
- Django 6.0.4 with a multi-app architecture (`home`, `products`, `cart`, `checkout`, `accounts`).
- SQLite in development; PostgreSQL in production, wired through `DATABASE_URL` / `dj-database-url` (see [Deployment](#deployment)).
- Server-rendered templates with Bootstrap 5 utilities and `django-crispy-forms` (bootstrap5 pack).
- Session-based cart and in-progress gift state; nothing is persisted until checkout completes.
- Stripe Payment Element for payment, with a webhook handler as the reliability fallback that actually sends the confirmation and gift emails.
- `django-allauth` for authentication, with mandatory email verification.
- A single custom stylesheet (`static/css/base.css`) built around CSS custom properties, with fluid typography via `clamp()` and breakpoints at 768/1024/1440/1800px.
- Three.js renders and animates the rotating 3D can model on the home page hero.

### Skeleton

The skeleton stage was about placement, before any colour or styling: a fixed
navbar carrying the main links (Home, All Products, Gift a Can, Cart, and the
account links once signed in), and the primary action button (Add to Cart,
Checkout, Complete Order) kept low on the page where the eye finishes reading.
These choices were worked out in the wireframes below.

### Wireframes

Wireframes and the high-fidelity design were both built in Figma:

**[Milky — Figma file](https://www.figma.com/design/90A4C1NyUtrnebcMyJtTlb/MILKY?node-id=1-5049)**

<details>
<summary>Mobile wireframes</summary>

<p align="center">
  <img src="docs/images/wireframes/wireframes-mobile.png" alt="Milky mobile wireframes" style="width: 90%; max-width: 900px; height: auto;">
</p>
</details>

<details>
<summary>Tablet wireframes</summary>

<p align="center">
  <img src="docs/images/wireframes/wireframes-tablet.png" alt="Milky tablet wireframes" style="width: 90%; max-width: 900px; height: auto;">
</p>
</details>

<details>
<summary>Desktop wireframes</summary>

<p align="center">
  <img src="docs/images/wireframes/wireframes-desktop.png" alt="Milky desktop wireframes" style="width: 90%; max-width: 900px; height: auto;">
</p>
</details>

From the wireframes on, the layout was refined directly in the browser across
the 768 / 1024 / 1440 / 1800px breakpoints.

### Surface

#### Visual Style

**Design:**
A warm, playful storefront built around soft rounded cards, layered product imagery, and a cream-and-brown color language. Product cards are composed from three stacked images (background, floating objects, can) for a bit of depth, and a rotating 3D can model anchors the home page hero.

**Typography:**
Three Google Fonts: `Bebas Neue` for headings, `Poppins` for body text, and `Patrick Hand` as a handwritten accent on a few decorative labels (such as the "It's Still Good For You" section). Type sizes are fluid (`clamp()`-based) rather than jumping at fixed breakpoints, so headings and body text scale smoothly with the viewport.

#### Colors
The palette centers on warm cream backgrounds with brown text, gold for primary calls to action, and green for success/discount highlights.

| Token | Hex | Use |
|---|---|---|
| `--light-cream` | `#faeade` | Page background |
| `--brown` | `#523122` | Primary text |
| `--light-brown` | `#8c5e4a` | Secondary text |
| `--gold` | `#fbcb62` | Primary CTA buttons |
| `--green` | `#198754` | Success states, discounts |
| `--danger` | `#dc3545` | Errors |
| `--card-background` | `#fafafa` | Card surfaces |
| `--footer-background` | `#e9cfb7` | Footer |

<p align="center">
  <img src="docs/images/Color.png" alt="Milky color palette" style="width: 32%; max-width: 300px; height: auto;">
</p>

## Technical Architecture

### Admin Page

The Django admin interface manages the core catalogue and order data:

**Products:**
- List view with name, flavor, SKU, price, stock, and thumbnail
- Filter by availability and flavor
- Full add/edit/delete access to every product field, including the three layered card images

<p align="center">
  <img src="docs/images/Django/Django_Products.png" alt="Django admin product management" style="width: 70%; max-width: 700px; height: auto;">
</p>

**Reviews:**
- List view with reviewer name, product, a ★/☆ star display, and a truncated comment
- Search by reviewer name or product, filter by rating or product
- Reviewer's username resolved and shown via the linked order, where one exists

<p align="center">
  <img src="docs/images/Django/Django_Reviews.png" alt="Django admin review management" style="width: 70%; max-width: 700px; height: auto;">
</p>

**Orders:**
- List view with reference code, customer, email, status, date, and totals
- Search by reference code or customer name, filter by status or date
- Grouped fieldsets (Order Info / Financials / Delivery Details / Invoice Details), with computed fields like `grand_total` shown read-only
- Inline, editable order items with a custom "same as delivery" admin widget that copies delivery details into the invoice fields
- Editing or deleting order items in the admin automatically recalculates the parent order's total

<p align="center">
  <img src="docs/images/Django/Django_Orders.png" alt="Django admin order management" style="width: 70%; max-width: 700px; height: auto;">
</p>

**Customers, Contacts & Users:**
- Registered in the admin (create/view/edit/delete), using Django's default list views — no custom search or filtering configured for these three yet.

### CRUD Operations

**Milky** implements CRUD across its core features, split between the customer-facing UI and the Django admin:

#### **Products**
- **Create / Update / Delete**: superusers only, directly from the storefront (Products Management), or via the Django admin
- **Read**: everyone — home page (featured), All Products (full catalogue), and the product detail page

#### **Reviews**
- **Create**: authenticated users, from the product detail page
- **Read**: everyone, paginated 3 per page on the product detail page
- **Update / Delete**: not available to the review's author from the front end; superusers can edit or delete any review via the Django admin

#### **Cart (session-based, no database record)**
- **Create / Update / Delete**: add a product, change its quantity, or remove it — all reflected instantly (AJAX) without a page reload

#### **Gift a Can**
- **Create**: pick a product and a recipient, held in the session until the order is placed — limited to one gift per order
- **Read**: the gift line is shown in the cart and at checkout alongside the regular items
- **Delete**: removable from the cart before checkout to free up the "one gift" slot

#### **Orders**
- **Create**: created on successful Stripe payment (either via the browser return flow or, as a reliability fallback, via the Stripe webhook)
- **Read**: the order confirmation page, and the "Orders" tab of the account profile
- **Update**: order status only, via the Django admin (Pending / Completed / Cancelled) or automatically on a failed payment webhook

#### **Account (Customer profile & saved Contacts)**
- **Create**: a `Customer` record is created automatically the first time a signed-in user reaches checkout or their profile
- **Read / Update**: the "My Profile" tab of the account page
- **Contacts (saved gift recipients)**: full create, read, update, and delete from the "Contacts" tab

### User Feedback

**Toast Notifications** (four variants, driven by Django's messages framework):
- Success, error, warning, and info toasts, positioned as a fixed banner and capped at the site's max content width so they never sit past the page's right edge on wide screens
- Success toasts adapt their title and icon by context (cart, cart update, cart removal, product, review, gift, order, profile, contact)
- Adding an item to the cart shows a full mini-cart preview inline inside the toast: thumbnails, quantities, running total, and a free-delivery progress banner
- Every toast has a manual close button and auto-hides after 6 seconds (`toast.js`)

**Confirmation Modals** (triggered before destructive actions):
- **Delete Product Modal**: shown to superusers before permanently deleting a product, from any page that shows a product card
- **Delete Contact Modal**: shown before removing a saved gift recipient from the Contacts tab

**Empty States**:
- **Empty Cart**: "Your cart is empty" with a Shop Now call to action
- **No Reviews**: "No reviews yet" / "Be the first to share your thoughts!" on the product detail page
- **No Orders**: "No orders found yet." on the profile's Orders tab
- **No Contacts**: "No contacts yet." on the profile's Contacts tab

**Real-Time Feedback**:
- AJAX quantity updates and removals in the cart, with totals and the free-delivery banner updating in place
- AJAX-paginated reviews on the product detail page (no full page reload)
- Interactive star-rating picker on the review form (click/hover to set 1–5 stars)
- The Stripe Payment Element mounts lazily, only once the payment section scrolls into view

**Form Validation Errors**:
- Django/crispy-forms field errors are shown inline, directly below the relevant input
- Required fields are marked, and Stripe's own card-input validation surfaces inline card errors at checkout

### Database Schema

The app uses Django's ORM — SQLite in development, PostgreSQL in production.

#### ERD — Entity Relationship Diagram

```
USER ||--o{ USERCUSTOMER : "linked via"
USERCUSTOMER }o--|| CUSTOMER : "resolves to"
CUSTOMER ||--o{ CONTACT : "has"
CUSTOMER ||--o{ ORDER : "places"
ORDER ||--o{ ORDERITEM : "contains"
PRODUCT ||--o{ ORDERITEM : "ordered as"
PRODUCT ||--o{ REVIEW : "receives"
ORDER ||--o{ REVIEW : "credits (optional)"
CONTACT ||--o{ ORDERITEM : "gifted to (optional)"
```

<p align="center">
  <img src="docs/images/ERD.png" alt="Milky ERD" style="width: 100%; max-width: 1000px; height: auto;">
</p>

**ERD note:** `User` ↔ `Customer` is resolved through an explicit `UserCustomer` join model rather than a `OneToOneField`. It isn't enforced as 1:1 at the database level, but the application always looks it up as if it were (`.filter(user=request.user).first()`).

**Legend:**
- **Solid line** — enforced One-to-One (via `OneToOneField`)
- **Dashed line** — ForeignKey relationship 1:N
- **PK** — Primary Key
- **FK** — Foreign Key

---

#### Core Models & Relationships

**1. User (Django's built-in auth model)**
- **Purpose:** authentication and session identity
- **Key fields:** `id`, `username`, `email`, `password` (hashed), `is_active`, `is_staff`, `date_joined`

---

**2. `accounts.UserCustomer`** — join table between `User` and `Customer`
- **Foreign Keys:** `user` (→ `auth.User`, `CASCADE`), `customer` (→ `Customer`, `CASCADE`)
- **Fields:** just `id` and the two foreign keys
- **Note:** logically 1:1 (app code always resolves it with `.filter(user=...).first()`), but not enforced with a DB-level uniqueness constraint.

---

**3. `accounts.Customer`**
- **Purpose:** the human profile behind an order — not tied 1:1 at the DB level, resolved via `UserCustomer`
- **Fields (all optional — the profile is filled in gradually):**
  - `name`, `surname` (CharField(255), blank)
  - `phone_number` (CharField(20), blank)
  - `address`, `city` (CharField(255), blank)
  - `county` (CharField(100), null/blank)
  - `postal_code` (CharField(20), blank)
  - `country` (CountryField via `django-countries`, null/blank)

---

**4. `accounts.Contact`** — a saved gift recipient ("friend")
- **Foreign Key:** `customer` (→ `Customer`, `CASCADE`)
- **Fields:** `name`, `surname` (CharField(255), required), `phone_number` (CharField(20), required), `email` (EmailField, required)
- **Address (all required except `county`):** `address`, `city` (CharField(255)), `county` (CharField(100), null/blank), `postal_code` (CharField(20)), `country` (CountryField)
- `ip_address` (GenericIPAddressField, captured server-side at creation)
- **Note:** unlike `Customer`, a `Contact`'s address is required — it is created at the moment of an actual gift, not built up gradually.

---

**5. `products.Product`**
- **Fields:**
  - `sku` (CharField(255), unique, auto-generated `MILK-XXXXXX`)
  - `name` (CharField(255), required)
  - `flavor` (CharField(50), choices: chocolate, vanilla, fruity, caramel, nutty, special)
  - `description` (TextField, soft cap 500 chars)
  - `price` (DecimalField, 6 digits / 2 decimal places)
  - `product_image` (ImageField, null/blank) — single image used on the detail page, cart, and checkout
  - `product_image_url` (URLField, null/blank) — an alternative to uploading: point `product_image` at an external URL instead
  - `background_image`, `objects_image`, `can_image` (ImageField, null/blank) — the three layered images used to build each product card
  - `stock` (PositiveIntegerField, nullable)
  - `is_available` (BooleanField, default `True`)
  - `featured` (BooleanField, default `False`) — shown on the home page
  - `display_order` (PositiveIntegerField, default `0`)
- **Meta:** ordered by `display_order`, then `name`

---

**6. `products.Review`**
- **Foreign Keys:** `product` (→ `Product`, `CASCADE`, `related_name="reviews"`), `order` (→ `checkout.Order`, `SET_NULL`, optional — links a review to the order that "earned" it)
- **Fields:** `name`, `surname` (CharField(255), required), `rating` (PositiveIntegerField, 1–5, `MinValueValidator`/`MaxValueValidator`), `comment` (TextField(500), blank/null)
- No `Meta` ordering — reviews paginate in insertion order

---

**7. `checkout.Order`**
- **Foreign Key:** `customer` (→ `accounts.Customer`, `SET_NULL`, nullable — guest orders have no linked customer)
- **Fields:**
  - `reference_code` (CharField(100), unique, auto-generated `ORDER-XXXXXXXX`)
  - `stripe_pid` (CharField(254), nullable)
  - `status` (IntegerField, choices: 0 Pending / 1 Completed / 2 Cancelled)
  - `created_at` (DateTimeField, auto)
  - `order_total` (DecimalField) — sum of its items, recalculated automatically whenever an item is saved
  - `delivery_cost` (DecimalField, default `0.00`) — recalculated on every save (free from $25, otherwise $3.99)
  - `promo_discount_percent` (DecimalField, nullable) — set when the order includes a gift
  - Separate `delivery_*` (required) and `invoice_*` (optional) address blocks, plus `email` (required)
- **Computed:** `grand_total` property = `order_total + delivery_cost`, minus the promo discount if set

---

**8. `checkout.OrderItem`**
- **Foreign Keys:** `order` (→ `Order`, `CASCADE`, `related_name="items"`), `product` (→ `Product`, `CASCADE`), `gift_contact` (→ `accounts.Contact`, `SET_NULL`, optional)
- **Fields:** `sku`, `unit_price` (snapshotted from the product at purchase time), `quantity`, `total_price` (auto-computed), `is_gift` (BooleanField, default `False`), `gift_message` (TextField, blank)
- **Side effect:** saving an `OrderItem` also recalculates and re-saves its parent `Order`'s `order_total`

---

#### Relationships Summary

| Relationship | Models involved | Type | Enforcement |
|---|---|---|---|
| User ↔ Customer | User, UserCustomer, Customer | Effectively One-to-One | Join model, app-enforced only |
| Customer → Contact | Customer, Contact | One-to-Many | `ForeignKey` + `CASCADE` |
| Customer → Order | Customer, Order | One-to-Many | `ForeignKey` + `SET_NULL` |
| Order → OrderItem | Order, OrderItem | One-to-Many | `ForeignKey` + `CASCADE` |
| Product → OrderItem | Product, OrderItem | One-to-Many | `ForeignKey` + `CASCADE` |
| Product → Review | Product, Review | One-to-Many | `ForeignKey` + `CASCADE` |
| Order → Review | Order, Review | One-to-Many, optional | `ForeignKey` + `SET_NULL` |
| Contact → OrderItem | Contact, OrderItem | One-to-Many, optional | `ForeignKey` + `SET_NULL` |

---

#### Data Flow Examples

**Example 1 — First checkout**
1. A signed-in user with no `Customer` yet reaches checkout.
2. A blank `Customer` and its `UserCustomer` link are created automatically.
3. The delivery form is saved back onto that `Customer` if "save this delivery info" is checked.

**Example 2 — Gift a Can**
1. The user picks a product and a recipient (existing `Contact`, or creates a new one) on the Gift a Can page.
2. The selection is held in `request.session['gift']` — nothing is written to the database yet.
3. On successful payment, an `OrderItem` is created with `is_gift=True` and `gift_contact` set, and a gift confirmation email is sent to the recipient.

**Example 3 — Order creation has two paths**
1. The browser is redirected back from Stripe to `checkout_success`, which creates the `Order` + `OrderItem`s directly — this is the happy path.
2. Independently, Stripe's `payment_intent.succeeded` webhook creates the same order from the PaymentIntent's metadata **if it doesn't already exist** (looked up by `stripe_pid`) — this is the reliability fallback, and it's also the only path that actually sends the confirmation and gift emails.

#### Schema Characteristics

- **One relational database**, accessed only through the Django ORM and migrations — no raw SQL.
- **Delete behaviour is chosen per relationship:** `CASCADE` for tightly-owned rows (an `Order`'s items, a `Customer`'s contacts, a `Product`'s reviews), and `SET_NULL` where a record should outlive its parent (a guest `Order` when its `Customer` is removed, a `Review` when its linked `Order` goes, a gifted `OrderItem` when the `Contact` is deleted).
- **Money is stored as `DecimalField`**, never a float.
- **Purchase data is snapshotted:** `OrderItem` copies the product's `sku` and `unit_price` at checkout, so later product edits never rewrite past orders.
- **Totals are denormalised** onto `Order` (`order_total`, `delivery_cost`) and kept in sync by `save()` overrides on `Order` and `OrderItem`.
- **Transient state stays out of the database:** the cart and the in-progress gift live in the session; the first row is written only when an order is placed.
- **`User` ↔ `Customer` is a deliberate join model** (`UserCustomer`) rather than a `OneToOneField` — treated as 1:1 in code but not constrained at the database level.

## Features

### Existing Features

#### **Header & Navigation**

- **Public Navigation:**
  - Home
  - All Products
  - Gift a Can
  - Cart
  - Register
  - Sign In

- **Authenticated Navigation:**
  - Home
  - All Products
  - Gift a Can
  - Cart
  - My Profile
  - Sign Out
  - Products Management *(superusers only)*

<p align="center">
  <img src="docs/images/Navbar.png" alt="Milky navigation bar" style="width: 90%; max-width: 900px; height: auto;">
</p>

- On mobile, the navigation collapses into a toggle menu that closes when you click outside it.

#### **Home Page**

- **Hero Section:**
  - An animated, rotating 3D can (rendered with Three.js) over a brand watermark
  - A "Shop Now" call to action
- **Our Favorites:**
  - A grid of the products flagged `featured`
  - Each card is built from three layered images, with a subtle mouse-tilt parallax effect
  - Superusers see an Edit / Delete overlay on every card
- **It's Still Good For You:** a benefits section with a stats card (Calcium / Protein / Vitamin D)
- **Moments That Taste Better:** a lifestyle photo section

<p align="center">
  <img src="docs/images/Home.png" alt="Milky home page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **All Products**

- Full product grid, using the same card component and superuser overlay as the home page
- Each card links through to its Product Detail Page

<p align="center">
  <img src="docs/images/All_Products.png" alt="All products page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Product Detail Page**

- **Product image:** the layered can visual, with a "Coming Soon" state when a product isn't available yet and an "Out of Stock" state at zero stock
- **Add to cart:** a quantity selector and an Add to Cart button
- **Product info:** benefit highlight icons and a nutrition-facts table (per 100ml / per 330ml)
- **Reviews:**
  - Paginated 3 per page, loaded via AJAX with no full reload, each with a star-rating display
  - A star-picker review form for signed-in users, or a "Sign In to leave a review" prompt for guests

<p align="center">
  <img src="docs/images/Product_Detail.png" alt="Product detail page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Gift a Can**

- **Logged out:** a promo landing page — hero image, a 3-step "how it works" explainer, and Sign In / Register calls to action
- **Logged in:** the full gift form —
  - A custom product picker
  - An optional personal message
  - Either a saved contact or new-friend fields
- **One gift per order:** if a gift is already in the session, the page shows a locked state instead

<p align="center">
  <img src="docs/images/Gift_a_Can.png" alt="Gift a Can page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Cart**

- **Line items:** an AJAX quantity stepper (clamped 1–99) and AJAX remove
- **Gift line:** a separate, non-editable line if a Gift a Can is in progress, with its own remove button
- **Order summary:** subtotal, delivery, gift discount, grand total, and a live free-delivery progress banner
- **Empty state:** cart icon, "Your cart is empty" message, and a Shop Now button

<p align="center">
  <img src="docs/images/Cart.png" alt="Cart page" style="width: 50%; max-width: 550px; height: auto;">
</p>

#### **Checkout Page**

- **Layout:** Details / Delivery / Invoice / Payment sections, in a two-column responsive layout from tablet width up, with a sticky order summary
- **Same as delivery:** a checkbox that hides / shows the invoice fields
- **Save details:** a "Save this delivery info to my profile" checkbox for signed-in users, or a login / register prompt for guests
- **Payment:**
  - Stripe Payment Element, mounted only once it scrolls into view
  - The "Complete Order" button stays disabled until Stripe reports the form is ready

<p align="center">
  <img src="docs/images/Checkout.png" alt="Checkout page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Order Confirmation**

- Reference code, itemised line items, price recap, delivery address, and a "Continue Shopping" call to action
- The same template doubles as the order-detail view reached from the profile's Orders tab

<p align="center">
  <img src="docs/images/Order_Confirmation.png" alt="Order confirmation page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Profile Page**

- **My Profile:** edit name, surname, phone, address, city, postal code, and country
- **Orders:** a list of past orders with a status badge (Pending / Completed / Cancelled) linking to the order detail view, or a "No orders found yet." empty state
- **Contacts:** saved gift recipients, with inline edit-in-place, a delete-confirmation modal, an "Add a Friend" form, or a "No contacts yet." empty state
- The active tab is remembered across redirects (for example, after adding a contact you land back on the Contacts tab)

<p align="center">
  <img src="docs/images/Profile.png" alt="Profile page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Products Management (Superuser Only)**

- **Add / Edit forms**, grouped into sections: Info, Cart & Checkout Image, Product Card Visuals (the three layered images), and Stock & Visibility
- **Custom file-upload widgets** showing the current image with a "Remove Image" option
- **Delete** has no dedicated page — it's triggered from a shared confirmation modal, available on any product card

<p align="center">
  <img src="docs/images/Products_Management.png" alt="Superuser products management" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Authentication Pages** (django-allauth)

All auth pages share the same split layout — a form on one side, an illustration on the other (hidden below tablet width).

- **Register:** email, username and password; a verification email is sent, and the account can't sign in until the email is confirmed
- **Sign In:** by email address and password
  - "Remember Me" controls session length only — checked keeps the session alive for two weeks after the browser closes, unchecked ends it when the browser closes
  - It doesn't pre-fill the form on a later visit — that's the browser's own password manager
- **Sign Out:** a confirmation page before the session is cleared
- **Password Reset:** request a link by email → open it → set a new password, with "sent" and "done" states in between
- **Password Change / Set:** change the password from the account while signed in
- **Email management:** add, remove, re-send verification, and set the primary email address

<p align="center">
  <img src="docs/images/Login.png" alt="Sign in page" style="width: 60%; max-width: 900px; height: auto;">
</p>

#### **Toast Notification System**

- Four variants — success, error, warning, info — with context-specific titles and icons
- Adding a product to the cart shows a live mini-cart preview inside the toast itself
- Fuller detail in [Technical Architecture → User Feedback](#user-feedback)

<p align="center">
  <img src="docs/images/Toast.png" alt="Toast notification with mini-cart preview" style="width: 50%; max-width: 450px; height: auto;">
</p>

#### **Modals**

Confirmation modals are shown before any destructive action, so nothing is deleted on a single click:

- **Delete Product Modal:** shown to superusers before permanently deleting a product, from any page with a product card
- **Delete Contact Modal:** shown before removing a saved gift recipient from the Contacts tab

<p align="center">
  <img src="docs/images/Delete_Modal.png" alt="Delete confirmation modal" style="width: 50%; max-width: 450px; height: auto;">
</p>

#### **Input Fields & Forms**

- All forms render through `django-crispy-forms` with the `crispy-bootstrap5` pack, so fields, labels and help text share one style
- Field errors show inline, right under the field they belong to; required fields are marked
- `django-countries` provides the country dropdown on the delivery and invoice forms
- **Custom widgets:**
  - A file-upload widget that previews the current image with a "Remove" toggle (Products Management)
  - A "Same as delivery" checkbox that shows / hides the invoice block (Checkout)
  - A click / hover star picker (review form)
  - A visual product picker (Gift a Can)
- Stripe's Payment Element handles the card fields and surfaces its own inline card errors

#### **Accessibility**

- Semantic landmarks on every page: `<header>`, `<nav>`, `<main>`, `<footer>`, and `<html lang="en">`
- Every `<img>` has an `alt` attribute
- Icon-only controls carry text alternatives: `aria-label` on the footer social links and the mobile menu toggle, plus `aria-expanded` / `aria-controls` on the toggle
- Toasts are announced to screen readers via `role="alert"`, `aria-live` and `aria-atomic`
- Most pages lead with a single `<h1>`; the home page currently uses `<h1>` for each of its display section titles ("Our Favorites", "It's Still Good For You", …), which is a known heading-structure issue to tidy up
- Dark-brown text on the cream background keeps body copy at a high contrast ratio

#### **Base Templates**

- `templates/base.html` is the single site-wide shell: `<head>` (fonts, Bootstrap, Font Awesome, `base.css`), the header / navbar, `{% block content %}`, the footer, and the toast container
- Shared partials live in `templates/includes/`: `main_nav.html`, `mobile_nav.html`, the four toast variants, and `delete_product_modal.html`
- `django-allauth`'s pages extend a themed `templates/allauth/` layout so they match the rest of the site
- The custom error pages extend `templates/errors/base_error.html`

#### **Footer**

- Social media links (X, Instagram, Facebook), each with an accessible label
- Copyright notice
- Consistent across every page

<p align="center">
  <img src="docs/images/Footer.png" alt="Website footer" style="width: 70%; max-width: 1200px; height: auto;">
</p>

#### **Responsiveness**

- Mobile-first, with custom breakpoints at 768px, 1024px, 1440px, and 1800px, plus a small tweak below 360px
- Fluid typography via `clamp()` instead of hard jumps between breakpoints
- The checkout page reflows into a two-column layout with a sticky order summary from tablet width up
- The whole site is capped at a 1800px max content width and centred, so fixed elements (like the toast banner) align to the content edge, not the raw screen edge, on ultra-wide screens

## Error Pages

All four custom error pages share the same branded layout: a breakpoint-swapped illustration, the status code, a short title, a plain-language message, and a single "Back to Home" call to action.

| Error Code | Title Shown | Message Shown |
|---|---|---|
| **404** | Page Not Found | "The page you're looking for doesn't exist or has been moved." |
| **403** | Access Forbidden | "You don't have permission to access this page." |
| **405** | Method Not Allowed | "This request method is not supported for this page." |
| **500** | Server Error | "Something went wrong on our end. Please try again in a moment." |

<p align="center">
  <img src="docs/images/Error_404.png" alt="404 error page" style="width: 20%; max-width: 300px;">
  <img src="docs/images/Error_403.png" alt="403 error page" style="width: 20%; max-width: 300px;">
  <img src="docs/images/Error_405.png" alt="405 error page" style="width: 20%; max-width: 300px;">
  <img src="docs/images/Error_500.png" alt="500 error page" style="width: 20%; max-width: 300px;">
</p>

## Site Map

<p align="center">
  <img src="docs/images/sitemap.png" alt="Milky site map" style="width: 90%; max-width: 900px; height: auto;">
</p>

## Future Features

- **Product search, filtering, and sorting** on the All Products page
- **Wishlists** — save a product for later without adding it to the cart
- **Subscriptions** — recurring delivery of a favorite flavor
- **Multiple gift recipients per order**, instead of the current one-gift limit
- **Editable/deletable reviews** from the front end, for the reviewer
- **Self-service account deletion**
- **Social login** (Google/Facebook) — `django-allauth` already supports it, no providers are configured yet
- **Order tracking / shipping notifications**
- **A loyalty or rewards program**
- **Live chat support**
- **Multiple photos per review**
- **Shipping a gifted can to the recipient's own address** — the friend's
  address is now collected and saved on the Contact, but the order itself
  still ships to the buyer's address; there's no support yet for a single
  order having two different delivery addresses

## Technologies Used

### Languages

* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CSS](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Python Packages

Installed via `requirements.txt`:

| Package | Purpose |
|---|---|
| [Django](https://www.djangoproject.com/) 6.0.4 | the web framework the whole project is built on |
| [django-allauth](https://docs.allauth.org/) | authentication, registration, and mandatory email verification |
| [django-crispy-forms](https://django-crispy-forms.readthedocs.io/) + [crispy-bootstrap5](https://pypi.org/project/crispy-bootstrap5/) | form rendering with the Bootstrap 5 template pack |
| [django-countries](https://pypi.org/project/django-countries/) | country fields on the delivery / invoice forms |
| [django-storages](https://django-storages.readthedocs.io/) + [boto3](https://pypi.org/project/boto3/) | static files and media on AWS S3 in production |
| [stripe](https://pypi.org/project/stripe/) | Stripe Python SDK — Payment Element and webhook handling |
| [dj-database-url](https://pypi.org/project/dj-database-url/) + [psycopg2](https://pypi.org/project/psycopg2/) | PostgreSQL connection in production |
| [gunicorn](https://pypi.org/project/gunicorn/) | WSGI server used on Heroku |
| [Pillow](https://pypi.org/project/pillow/) | image handling for uploaded product photos |
| [Brotli](https://pypi.org/project/Brotli/) | compression for static assets served from S3 |

Dev / QA tooling: [black](https://pypi.org/project/black/), [flake8](https://pypi.org/project/flake8/), [html5validator](https://pypi.org/project/html5validator/), [playwright](https://pypi.org/project/playwright/).

### Frameworks, Libraries & Software

* [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/): responsive layout, utility classes, and the base for the crispy-forms template pack (loaded via CDN)
* [Font Awesome](https://fontawesome.com/): icons throughout the UI (loaded via CDN)
* [Google Fonts](https://fonts.google.com/): `Bebas Neue`, `Poppins`, and `Patrick Hand`
* [Blender](https://www.blender.org/): modelling the 3D can shown on the home page hero
* [Three.js](https://threejs.org/): renders and animates that 3D can model in the browser
* [Adobe Photoshop](https://www.adobe.com/products/photoshop.html): editing product-card and photographic images (cut-outs, background removal)
* ChatGPT: generating the product can images
* [Stripe](https://stripe.com/docs): checkout and payment processing
* [Heroku](https://www.heroku.com/): application hosting
* [AWS S3](https://aws.amazon.com/s3/): static file and media storage in production
* [Git](https://git-scm.com/) & [GitHub](https://github.com/): version control and repository hosting
* [Figma](https://www.figma.com/): wireframes and high-fidelity design
* [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/): back-office management for products, reviews, and orders

## Testing

The tables below are the **manual test plan** for the project, covering authentication, CRUD, permissions, forms, UX, accessibility, and responsive layout. Each row is marked *To test* until it has been run and the result recorded. **There is no automated test suite** — every app's `tests.py` is still the default Django stub, and no CI pipeline is configured. `html5validator` and `playwright` are installed for the validator and browser checks (see below).

### Authentication

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Registration | Register with a new email and password | Account created, verification email sent (console backend in dev) | To test |
| Mandatory Email Verification | Try to sign in before verifying the email | Sign-in is blocked until the email is verified | To test |
| Sign In | Sign in with valid credentials | User is authenticated and redirected | To test |
| Invalid Sign In | Sign in with the wrong password | Error message shown, user stays on the sign-in page | To test |
| Password Reset | Request a reset link for a registered email | Reset flow completes and the new password works | To test |
| Sign Out | Click Logout in the navbar | User is signed out and redirected | To test |

### CRUD

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Add Product (superuser) | Fill in the product form and submit | Product created and immediately visible in the catalogue | To test |
| Edit Product (superuser) | Change a product's fields and save | Changes reflected everywhere the product appears | To test |
| Delete Product (superuser) | Confirm deletion from the shared modal | Product removed from the catalogue | To test |
| Add Review | Submit a star rating and comment on a product | Review appears in the paginated list | To test |
| Add / Edit / Delete Contact | Manage a saved gift recipient from the Contacts tab | Contact list updates immediately, in place | To test |
| Place Order | Complete checkout with a Stripe test card | Order created, confirmation page shown, order appears in Orders tab | To test |

### Permissions

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Products Management Access | Visit `/products/add/` while logged out or as a non-superuser | Redirected home with an error message | To test |
| Profile Access | Visit `/profile/` while logged out | Redirected to sign in | To test |
| Own-Data Scoping | Try to view another user's order confirmation page directly | Access denied unless it's the current session's own order | To test |
| Guest Order Confirmation | View the confirmation page right after a guest checkout | Accessible, since the reference code matches the session | To test |

### Forms

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Checkout Validation | Submit the checkout form with required fields missing | Inline validation errors shown, submission blocked | To test |
| Same as Delivery | Toggle the "same as delivery" checkbox at checkout | Invoice fields hide/show accordingly | To test |
| Gift Form Validation | Submit the Gift a Can form without selecting a product | Submission blocked client-side | To test |
| Review Rating Required | Submit the review form without picking a star rating | Submission blocked | To test |

### UX

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Cart Quantity Update | Use the +/- stepper on a cart line | Quantity and totals update in place via AJAX, no reload | To test |
| Toast Feedback | Add a product to the cart | Success toast appears with a live mini-cart preview | To test |
| Delete Confirmation | Click delete on a product (superuser) or a contact | Confirmation modal appears before anything is removed | To test |
| Review Pagination | Page through a product's reviews | Review list swaps via AJAX without a full reload | To test |

### Accessibility

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Keyboard navigation | Tab through the navbar, a product card, and the checkout form | Every interactive element is reachable and shows a visible focus state | *to test* |
| Screen reader — toasts | Trigger a success and an error toast with a screen reader running | Both are announced through their `aria-live` region | *to test* |
| Image alternatives | Inspect every `<img>` | Meaningful images have descriptive `alt`, decorative ones an empty `alt` | *to test* |
| Heading order | Run an outline check on each page type | One `<h1>` per page, no skipped levels (note: home page currently has several `<h1>`s) | *to test* |
| Colour contrast | Check brown-on-cream and brown-on-gold in a contrast checker | Meets WCAG AA for body text and buttons | *to test* |

### Validator Testing

| Tool | Target | Result |
|------|--------|--------|
| [W3C HTML Validator](https://validator.w3.org/) | Each rendered page (validated from view-source) | *to run — `html5validator` is installed* |
| [W3C CSS Validator (Jigsaw)](https://jigsaw.w3.org/css-validator/) | `static/css/base.css` | *to run* |
| [JSHint](https://jshint.com/) | Files in `static/js/` | *to run* |
| [flake8](https://flake8.pycqa.org/) / [black](https://black.readthedocs.io/) | Python source (`max-line-length = 140`, see `setup.cfg`) | *to run* |

Screenshots go in `docs/images/Testing/`.

### Browser Compatibility

| Browser | Version | Result |
|---------|---------|--------|
| Chrome | | *to test* |
| Firefox | | *to test* |
| Safari | | *to test* |
| Edge | | *to test* |

### Responsive Design

| Device Category | Screen Size | Test Result | Notes |
|----------------|-------------|-------------|-------|
| Mobile - Small | 390px × 844px | To test | |
| Tablet | 768px × 1024px | To test | Checkout switches to its two-column layout here |
| Tablet/Small Desktop | 1024px × 900px | To test | |
| Laptop | 1440px × 1000px | To test | |
| Desktop - Large | 2560px × 1300px | To test | Check the toast banner and body content stay aligned at the 1800px max content width |

### Performance

Lighthouse (Chrome DevTools) was used to audit performance, accessibility, best practices, and SEO. Reports are saved in `docs/images/LightHouse_Desktop/` and `docs/images/LightHouse_Mobile/`.

| Page | Performance | Accessibility | Best Practices | SEO |
|------|-------------|---------------|----------------|-----|
| Home | | | | |
| All Products | | | | |
| Product Detail | | | | |
| Cart | | | | |
| Checkout | | | | |

### Bugs Found, Fixed, and Unresolved

| Bug | Status | Notes |
|-----|--------|-------|
| Toast notifications pinned to the raw screen edge on screens wider than 1800px | Fixed | The toast wrapper used Bootstrap's `w-100` on a `position: fixed` element, which resolves against the viewport rather than the centered, max-width body. It's now capped at the same max content width and centered. |
| Horizontal overflow on the home page on mobile | Fixed | Two Bootstrap `.row`s sat directly inside a `<section>` with no `.container` parent, so the default negative row gutters bled past the viewport edge. Wrapping both rows in `.container` fixed it. |
| Account pages skipped from `<body>` straight to `<h2>`, with no `<h1>` anywhere on the page | Fixed | Promoted each account page's main heading to `<h1>`, with a sizing utility class so the visual size didn't change. |
| `checkout/views.py` calls `reverse("products")` and `reverse("cart")`, but those URL names don't exist (they're `all_products` and `view_cart`) | Unresolved | Would raise `NoReverseMatch` if those specific redirect paths are hit (checking out with an empty cart, or a missing product during order confirmation). |
| Hardcoded `DEBUG=True` and SQLite-only configuration | Unresolved | Not a bug in behavior, but a real gap before this project could go to production — see [Security & Current Limitations](#security--current-limitations). |

### Testing User Stories

| User Story | How It's Fulfilled | Features/Pages Used |
|------------|-------------------|---------------------|
| As a new visitor, I want to see the product range and understand the brand. | The home page opens with a hero and a featured-products showcase; All Products shows the full catalogue. | Home page, All Products |
| As a new visitor, I want to view a product's description, nutrition facts, and reviews. | The product detail page shows all three, plus a paginated review list. | Product Detail |
| As a new visitor, I want to add products to my cart and check out as a guest. | The cart and checkout flows don't require an account; `Order.customer` is nullable for guest orders. | Cart, Checkout |
| As a new visitor, I want to create an account so my details are saved for next time. | Registration via django-allauth, with delivery details saved to the `Customer` profile on request. | Register, Checkout ("save this delivery info") |
| As an existing user, I want my checkout form pre-filled. | The checkout view builds the form from the signed-in user's saved `Customer` record. | Checkout |
| As an existing user, I want to view my order history. | The profile's Orders tab lists past orders, linking to the reused confirmation template. | Profile — Orders tab |
| As an existing user, I want to save a friend as a contact for gifting. | The profile's Contacts tab supports full CRUD on saved gift recipients. | Profile — Contacts tab, Gift a Can |
| As an existing user, I want to reset my password. | django-allauth's password reset flow. | Password Reset |
| As an existing user, I want to leave a star rating and comment on a product. | The review form on the product detail page, restricted to authenticated users. | Product Detail |
| As a user, I want clear confirmation before a destructive action. | Shared confirmation modals for product deletion and contact deletion. | Products Management, Profile — Contacts tab |
| As a user, I want feedback after every action. | The toast notification system, plus inline form validation errors. | Site-wide |
| As a user, I want the site to work well across devices. | Fluid typography and four custom breakpoints (768/1024/1440/1800px), verified manually across mobile, tablet, laptop, and wide desktop. | Site-wide |

## Security & Current Limitations

- **Environment variables:** `SECRET_KEY`, `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, and `STRIPE_WH_SECRET` are all read from environment variables (via a local, gitignored `env.py` in development), not hard-coded.
- **CSRF protection:** Django's CSRF middleware is active; server-rendered forms include `{% csrf_token %}`, and the Stripe webhook endpoint is the only intentionally `@csrf_exempt` view (verified instead via the Stripe signature header).
- **Authentication & access control:** views that mutate data are gated with `@login_required`; the Products Management views additionally check `request.user.is_superuser` before allowing add/edit/delete. Order confirmation pages are scoped so a guest can only view the order matching their own session, and an authenticated user can only view their own orders.
- **Mandatory email verification:** `django-allauth` is configured with `ACCOUNT_EMAIL_VERIFICATION = "mandatory"`, so an account can't sign in until its email is confirmed.

**Not yet production-configured** — this project currently runs as a local development app, and the following would need addressing before a real deployment:
- `DEBUG = True` is hardcoded in `settings.py`, rather than driven by an environment variable.
- `ALLOWED_HOSTS` only includes `localhost`/`127.0.0.1`.
- The database is hardcoded to a local SQLite file — there's no `DATABASE_URL`/`dj_database_url` wiring for a hosted Postgres database yet.
- Static files have no `STATIC_ROOT` or WhiteNoise configuration, and media (product images) is stored on the local filesystem rather than a cloud storage backend like Cloudinary or S3 — neither will work as-is on Heroku's ephemeral filesystem.
- The email backend is the console backend (emails print to the terminal) — a real SMTP/transactional email provider would be needed in production.
- `requirements.txt` doesn't yet include a WSGI server (`gunicorn`), static file serving (`whitenoise`), or a Postgres driver (`psycopg2`) — see the deployment guide below for what to add.

## Deployment

### Heroku Deployment Guide

**Milky** is a standard Django app and can be deployed on Heroku, but — as noted above — it isn't deployment-ready out of the box yet. This guide covers both what needs to be added first and the deployment steps themselves.

#### What to add before deploying

1. Add these to `requirements.txt`:
   ```
   gunicorn
   whitenoise
   dj-database-url
   psycopg2-binary
   ```
   (Add `cloudinary` and `django-cloudinary-storage` too if you want product images stored off the local filesystem, which Heroku's ephemeral filesystem requires.)
2. Add a `Procfile` at the project root:
   ```
   web: gunicorn milky.wsgi:application
   ```
3. In `milky/settings.py`, switch `DEBUG` and `ALLOWED_HOSTS` to read from environment variables, wire up `dj_database_url.parse(os.environ.get("DATABASE_URL"))` in `DATABASES`, add WhiteNoise to `MIDDLEWARE` with `STATIC_ROOT` set, and configure a real `EMAIL_BACKEND`.

#### Prerequisites

- A Heroku account
- A hosted PostgreSQL database (Heroku Postgres, or an external provider)
- A Stripe account (test or live keys)
- A Cloudinary account, if you've added cloud media storage
- The code pushed to a GitHub repository

#### Environment Variables Required

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DATABASE_URL` | PostgreSQL connection string |
| `STRIPE_PUBLIC_KEY` | Stripe publishable key |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `STRIPE_WH_SECRET` | Stripe webhook signing secret |
| `CLOUDINARY_URL` | Only if cloud media storage has been added |

#### Step-by-Step Deployment Instructions

1. **Push code to GitHub**
   ```bash
   git push origin main
   ```
2. **Create a Heroku app** at [dashboard.heroku.com](https://dashboard.heroku.com) → "New" → "Create new app".
3. **Connect the GitHub repository** under the app's "Deploy" tab.
4. **Set the environment variables** above under "Settings" → "Reveal Config Vars".
5. **Deploy** via "Deploy" tab → "Manual deploy" → "Deploy Branch".
6. **Run migrations**: "More" → "Run console" → `python manage.py migrate`.
7. **Create a superuser**: "More" → "Run console" → `python manage.py createsuperuser`.
8. **Add the Stripe webhook endpoint** (`https://<your-app>.herokuapp.com/checkout/webhook/`) in the Stripe dashboard, and set `STRIPE_WH_SECRET` to the signing secret it gives you.
9. **Open the app** and load the product fixtures if the database is empty: `python manage.py loaddata products/fixtures/products.json products/fixtures/reviews.json`.

#### Production Checklist (Before Going Live)
- `DEBUG = False`
- `SECRET_KEY` set to a strong, random value
- `DATABASE_URL` pointing at a real Postgres database
- Static files collecting correctly (WhiteNoise + `collectstatic`)
- Media storage configured (Cloudinary/S3, not the local filesystem)
- A real email backend configured (not the console backend)
- Stripe webhook endpoint registered and `STRIPE_WH_SECRET` set
- HTTPS enabled (automatic on Heroku)

**Note:** local (`localhost:8000/admin/`) and Heroku
(`your-app.herokuapp.com/admin/`) use two separate databases — an account or
order created on one will not appear in the other. Always check the admin
that matches where the action actually happened.

## Credits

### Visual Design References

*To be filled in — add any sites, apps, or mood boards that inspired Milky's visual direction here.*

### Code References

#### **Backend - Django**
- [Django Official Documentation](https://docs.djangoproject.com/) — core framework, models, views, forms
- [django-allauth Documentation](https://docs.allauth.org/) — authentication, registration, and email verification flows
- [Django ORM Relationships](https://docs.djangoproject.com/en/stable/topics/db/models/) — ForeignKey/OneToOne relationships and cascade behavior
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/) — custom `ModelAdmin` configuration, inlines, and `save_formset` overrides

#### **Payments**
- [Stripe Payment Element Documentation](https://stripe.com/docs/payments/payment-element) — client-side integration
- [Stripe Webhooks Documentation](https://stripe.com/docs/webhooks) — server-side payment confirmation and signature verification

#### **JavaScript**
- [Three.js Documentation](https://threejs.org/docs/) — loading and animating the 3D can model
- [Intersection Observer API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) — lazy-mounting the Stripe Payment Element

#### **General References**
- [Stack Overflow](https://stackoverflow.com/) — troubleshooting specific implementation issues
- [Mozilla Developer Network (MDN)](https://developer.mozilla.org/) — web standards and API documentation
