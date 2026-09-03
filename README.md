# Milky

<p align="center">
  <img src="docs/images/milky-preview.png" alt="Milky responsive preview" width="100%">
</p>

## About

**Milky** is a full-stack B2C e-commerce website built with Django for a
milkshake-in-a-can drinks brand. Visitors can browse the product range, read and
leave reviews, add cans to a cart, and check out securely with Stripe.
Registered customers get a profile that stores their delivery details and a full
history of their past orders, so reordering a favourite takes only a few clicks.

A standout feature is **Gift a Can**: any logged-in customer can add a can to
their order as a gift, name a friend as the recipient, leave a message and get
10% off. When the payment succeeds, the friend gets an email letting them know,
no account needed on their side.

On the other side of the shop, site administrators manage the entire product
catalogue (creating, editing and removing cans, flavours and stock)
directly from the front end, without ever touching the Django admin or the database.

**Note:** This project was built for educational purposes as part of the
[Code Institute](https://codeinstitute.net/) Full Stack Development programme.

**[View the live application](https://milky-app-839f694f035d.herokuapp.com/)**

## Table of Contents

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

* [Technical Architecture](#technical-architecture)
   * [Admin Page](#admin-page)
   * [CRUD Operations](#crud-operations)
   * [User Feedback](#user-feedback)
   * [Database Schema](#database-schema)

* [Future Features](#future-features)

* [Technologies Used](#technologies-used)

* [Testing](#testing)
   * [Automated Tests](#automated-tests)
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
   * [Branching model](#branching-model)
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

**Milky** is a warm, playful storefront for a single milkshake-in-a-can drinks brand. The strategy has two sides: make browsing flavours and checking out feel effortless for the customer, and give the brand a low-friction way to turn buyers into referrers through the Gift a Can feature.

#### Target audience

**Customers**
- Shoppers who buy novelty drinks online
- Returning customers reordering a favourite and tracking past orders
- People who want to send a drink as a gift to a friend or family member
- People who discovered the brand through a gifted can and are coming back to buy
  for themselves

**Site owner**
- A small drinks brand managing its own catalogue, stock and orders from the browser without developer help

#### Business goals of the website
- Present the product range well enough to convert a first-time visitor into a buyer.
- Keep checkout friction low, guests can buy without an account, and Stripe handles payment.
- Turn one-time buyers into repeat customers by saving delivery info and order history behind an account.
- Use Gift a Can as a built-in referral loop: a customer gets 10% off, a friend gets a free introduction to the brand.

#### Customer goals of the website
- Quickly understand what Milky is and see the available flavours.
- Get enough detail (description, nutritional information, reviews) to decide before buying.
- Add products to a cart and check out quickly, with or without creating an account.
- Send a can as a gift to a friend in a couple of clicks.
- Manage delivery/invoice details and revisit past orders without re-entering everything.

### User Stories

**New Visitor**
- As a new visitor, I want to see the product range and understand the brand, so I can decide if it's for me.
- As a new visitor, I want to view a product's description, nutritional information, and customer reviews, so I can make an informed choice.
- As a new visitor, I want to add products to my cart and check out as a guest, so I don't have to register just to buy something.
- As a new visitor, I want to create an account, so I can save my delivery details and reuse them at checkout next time.

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

#### In Scope
- Product catalogue with a featured selection on the home page and a full grid on All Products.
- Product detail page: nutritional information, benefit highlights, paginated reviews, and a review submission form for authenticated users.
- Session-based cart (add / update quantity / remove) with a live free-delivery progress banner, no account required.
- Gift a Can: pick a product and a recipient (saved contact or a new one), add an optional message, get 10% off the order.
- Stripe Payment Element checkout, with a delivery address and an optional separate invoice address.
- Order confirmation page, reused as the order-detail view from the account's order history.
- Transactional emails: an HTML order-confirmation email to the buyer and a "you've been gifted a can" email to the recipient, both sent when the Stripe webhook confirms payment.
- Account system (django-allauth): register, sign in/out, mandatory email verification, password reset/change, email management.
- Profile page with three tabs: edit personal details, view order history, manage saved gift contacts (full CRUD).
- Superuser-only Products Management: add, edit, and delete products directly from the storefront UI.
- Toast notification system (success / error / warning / info) with a dynamic mini-cart preview on "added to cart" toasts.
- Custom branded 404 / 403 / 405 / 500 error pages.

#### Out of Scope
- Product search, filtering, or sorting.
- Wishlists or saved-for-later items.
- Subscriptions / recurring orders.
- Multiple gift recipients per order (currently limited to one gift per order).
- Shipping a gifted can to the recipient's own address (the recipient's address is saved, but the order still ships to the buyer).
- Editing or deleting an existing review once submitted.
- Self-service account deletion.
- Social login (Google/Facebook). allauth is installed but no providers are configured.
- Real-time order tracking or shipping notifications.
- Loyalty points or a rewards program.
- Live chat support.
- Automatic stock management, decrementing a product's stock on purchase and blocking orders above the available quantity.
- Discount or promo codes at checkout (Gift a Can's 10% is applied automatically).
- Guest order look-up, letting a guest retrieve a past order without an account.

### Structure

The home page leads with a hero (an animated 3D can rendered with Three.js) and a "Shop Now" call to action, followed by a featured-products showcase, a nutrition/benefits section, and a closing lifestyle section. From there, the flow is intentionally linear: browse products → view a product's detail page → add to cart → check out. A persistent navbar keeps Home, All Products, Gift a Can, and the cart within reach at all times (collapsing to a burger menu and a dropdown on smaller screens), with the authenticated links (My Profile, Products Management for superusers, Sign Out) appearing once signed in. A footer with brand imagery and social links sits on every page.

Milky is a multi-page application (MPA) with server-side rendering via Django, each route renders a dedicated template rather than switching views inside a single-page app, with a few AJAX-enhanced interactions (cart quantity, review pagination). The cart and the in-progress gift selection live in the session, not the database.

Key sections and navigation flow:
- Home: hero with 3D can, featured products, nutrition/benefits section, lifestyle section.
- All Products: full catalogue grid.
- Product Detail: description, nutritional information, reviews, add to cart.
- Gift a Can: promo landing page for guests, full gift form for logged-in users.
- Cart: line items, gift line (if any), order summary.
- Checkout: delivery and invoice form with the Stripe Payment Element.
- Order Confirmation: reused for both the post-checkout success page and the profile's order-history detail view.
- Auth: register, sign in, password reset, email verification (django-allauth).
- Profile: My Profile / Orders / Contacts tabs.
- Products Management (superuser only): add/edit/delete products.
- Footer: brand imagery and social links (X, Instagram, Facebook), on every page.

#### Technical Implementation
- Django 6.0.4 with a multi-app architecture (`home`, `products`, `cart`, `checkout`, `accounts`).
- SQLite in development, PostgreSQL in production, wired through `DATABASE_URL` / `dj-database-url` (see [Deployment](#deployment)).
- Static files and media served from AWS S3 in production via `django-storages` and a small `custom_storages.py`.
- Photographic and illustrated assets (site imagery and product-card layers) are stored as WebP to keep page weight down. Small UI icons stay as PNG.
- Server-rendered templates with Bootstrap 5 utilities and `django-crispy-forms` (bootstrap5 pack).
- URLs follow one convention throughout: lower-case, hyphen-separated path segments (`/profile/order-history/`, `/checkout/cache-checkout-data/`, `/products/1/add-review/`), and every link is generated with `{% url %}` / `reverse()` from the route name, never hard-coded.
- Session-based cart and in-progress gift selection. Neither is written to the database until an order is placed.
- Stripe Payment Element for payment, with a webhook handler as the reliability fallback that actually sends the confirmation and gift emails.
- Transactional emails rendered from HTML and plain-text templates, with a shared stylesheet (`templates/emails/_email_styles.css`) and helpers in `milky/email_utils.py`.
- `django-allauth` for authentication, with mandatory email verification.
- A single custom stylesheet (`static/css/base.css`) built around CSS custom properties, with fluid typography via `clamp()` and breakpoints at 768/1024/1440/1800px.
- Three.js renders the home-page hero can: a glTF model on a transparent WebGL canvas, lit with an image-based studio environment and given a continuous gentle left-right swing (no user interaction). It resizes with its container.

### Skeleton

The skeleton stage was about placement, before any colour or styling, a fixed
navbar carrying the main links (Home, All Products, Gift a Can, Cart, and the
account links once signed in), and the primary action button (Add to Cart at the
end of the product block, Checkout at the foot of the cart summary, Complete
Order at the end of the checkout form) placed where the eye finishes reading each
step. These choices were worked out in the wireframes below.

### Wireframes

The wireframes and the high-fidelity design were built in Figma:

**[Full Wireframes on Figma here](https://www.figma.com/design/90A4C1NyUtrnebcMyJtTlb/MILKY?node-id=1-5049)**

<p align="center"><strong>Mobile wireframes</strong></p>
<p align="center">
  <img src="docs/wireframes/wireframe-mobile.png" alt="Milky mobile wireframes" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>Desktop wireframes</strong></p>
<p align="center">
  <img src="docs/wireframes/wireframe-desktop.png" alt="Milky desktop wireframes" style="width: 90%; max-width: 900px; height: auto;">
</p>

From the wireframes on, the layout was refined directly in the browser across
the 768 / 1024 / 1440 / 1800px breakpoints.

### Surface

#### Visual Style

**Design:**
A warm, playful storefront built around soft rounded cards, pill-shaped buttons, and a cream-and-brown colour language warmed with gold call-to-action accents. Product cards are composed from three stacked images (background, floating objects, and the can itself) layered for depth, with the product name set in bold uppercase over a soft gradient. On hover, the object and can layers drift with the cursor in a parallax effect against the fixed background. The home page hero is anchored by a rotating 3D can, and recurring decorative motifs (flowing wave dividers between sections, bubble shapes, and hand-drawn commas and arrows) carry the brand's lighthearted tone throughout.

**Typography:**
Three Google Fonts: `Bebas Neue` for headings, `Poppins` for body text, and `Patrick Hand` as a handwritten accent on a few decorative labels (such as the "It's Still Good For You" section). Type sizes are fluid (`clamp()`-based) rather than jumping at fixed breakpoints, so headings and body text scale smoothly with the viewport.

#### Colors
The palette centers on warm cream backgrounds with brown text, gold for primary calls to action, and green for success/discount highlights.

<div align="center">
  <table>
    <tr>
      <td valign="middle" width="65%" align="center">
        <table>
          <thead>
            <tr>
              <th align="left">Token</th>
              <th align="left">Hex</th>
              <th align="left">Use</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>--light-cream</code></td>
              <td>#faeade</td>
              <td>Page background</td>
            </tr>
            <tr>
              <td><code>--brown</code></td>
              <td>#523122</td>
              <td>Primary text</td>
            </tr>
            <tr>
              <td><code>--light-brown</code></td>
              <td>#8c5e4a</td>
              <td>Secondary text</td>
            </tr>
            <tr>
              <td><code>--gold</code></td>
              <td>#fbcb62</td>
              <td>Primary CTA buttons</td>
            </tr>
            <tr>
              <td><code>--green</code></td>
              <td>#198754</td>
              <td>Success states, discounts</td>
            </tr>
            <tr>
              <td><code>--danger</code></td>
              <td>#dc3545</td>
              <td>Errors</td>
            </tr>
            <tr>
              <td><code>--card-background</code></td>
              <td>#fafafa</td>
              <td>Card surfaces</td>
            </tr>
            <tr>
              <td><code>--footer-background</code></td>
              <td>#e9cfb7</td>
              <td>Footer</td>
            </tr>
          </tbody>
        </table>
      </td>
      <td valign="middle" width="35%" align="center">
        <img src="docs/images/colors.png" alt="Milky colour palette" width="100%" style="max-width: 320px;">
      </td>
    </tr>
  </table>
</div>

## Technical Architecture

### Admin Page

The Django admin interface manages the core catalogue and order data:

**Products:**
- List view with name, flavour, SKU, price, stock, and the product image field (ordered by SKU)
- Filter by availability and flavour
- No search box configured
- Full add/edit/delete access to every product field, including the three layered card images

<p align="center">
  <img src="docs/django/admin-products.png" alt="Django admin product management" style="width: 90%; max-width: 1100px; height: auto;">
</p>

**Reviews:**
- Each row shows the reviewer's name and surname, their account username, the product, the star rating, and a short preview of the comment
- Sorted by rating, highest first
- Search by reviewer name, surname, or product
- Filter by rating or product
- The username column is blank unless the review is tied to an order from that account

<p align="center">
  <img src="docs/django/admin-reviews.png" alt="Django admin review management" style="width: 90%; max-width: 1100px; height: auto;">
</p>

**Orders:**
- List view with reference code, customer (guests flagged), email, status, date, order total and delivery cost (newest first)
- Search by reference code or customer name
- Filter by status or date
- Grouped fieldsets (Order Info / Financials / Delivery Details / Invoice Details), with computed fields like `grand_total` shown read-only
- Order line items are editable inline, with unit price, line total and SKU shown read-only
- Editing or deleting line items automatically recalculates the parent order's total
- A JS-injected "Same as delivery address" checkbox on the Invoice fieldset copies the delivery fields across when ticked and clears them when unticked, and self-checks on load when the two already match

<p align="center"><strong>Order list view</strong></p>
<p align="center">
  <img src="docs/django/admin-orders.png" alt="Django admin order list view" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Order detail: Order Info and Financials fieldsets</strong></p>
<p align="center">
  <img src="docs/django/order.png" alt="Django admin order detail, Order Info and Financials fieldsets with grand total read-only" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Order detail: Delivery Details fieldset</strong></p>
<p align="center">
  <img src="docs/django/delivery-order.png" alt="Django admin order detail, Delivery Details fieldset" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Order detail: Invoice Details fieldset and inline order items</strong></p>
<p align="center">
  <img src="docs/django/invoice-order.png" alt="Django admin order detail, Invoice Details fieldset with the Same as delivery address checkbox and the inline order items" style="width: 90%; max-width: 1100px; height: auto;">
</p>

**Customers, Contacts & account links:**
- `Customer` is the delivery/billing profile behind an order
- `Contact` is one saved gift recipient (a "friend") belonging to a customer
- `UserCustomer` is the link row joining a `User` to their `Customer`
- All three use the default Django admin, with no custom list display, search or filtering. The `User` model keeps Django's built-in admin.

### CRUD Operations

**Milky** implements CRUD across its core features, split between the customer-facing UI and the Django admin:

#### **Products**
- **Create / Update / Delete**: superusers only, directly from the storefront (Products Management), or via the Django admin. A product that appears in a past order cannot be hard-deleted, it is hidden from the shop (`is_available` off) instead, so order history stays intact
- **Read**: everyone, on the home page (featured selection), All Products (full catalogue), and the product detail page

#### **Reviews**
- **Create**: authenticated users, from the product detail page
- **Read**: everyone, paginated 3 per page on the product detail page
- **Update / Delete**: intentionally not exposed to the review's author on the front end, reviews are final once posted. Superusers can still edit or delete any review through the Django admin

#### **Cart (session-based, no database record)**
- **Create / Update / Delete**: add a product, change its quantity, or remove it, all reflected instantly (AJAX) without a page reload

#### **Gift a Can**
- **Create**: pick a product and a recipient, held in the session until the order is placed, limited to one gift per order
- **Read**: the gift line is shown in the cart and at checkout alongside the regular items
- **Delete**: removable from the cart before checkout to free up the "one gift" slot

#### **Orders**
- **Create**: created on successful Stripe payment. The browser return flow creates it first as Pending, if that flow is interrupted, the Stripe webhook creates it instead as a reliability fallback.
- **Read**: the order confirmation page, and the "Orders" tab of the account profile
- **Update**: order status only (Pending / Completed / Cancelled). The `payment_intent.succeeded` webhook moves an order to Completed and sends the emails, the `payment_intent.payment_failed` webhook moves it to Cancelled. A staff user can also set the status by hand in the Django admin.

#### **Account (Customer profile)**
- **Create**: a `Customer` record is created automatically the first time a signed-in user reaches checkout, or the first time they save the "My Profile" form
- **Read / Update**: the "My Profile" tab of the account page

#### **Contacts (saved gift recipients)**
- **Create / Read / Update / Delete**: full CRUD from the "Contacts" tab of the account page

### User Feedback

**Toast Notifications** (four variants, driven by Django's messages framework):
- Success, error, warning, and info toasts, positioned as a fixed banner and capped at the site's max content width so they never sit past the page's right edge on wide screens
- Each of the four variants has its own icon, success toasts also adapt their title by context (cart, cart update, cart removal, product, review, gift, order, profile, contact)
- Cart toasts show a full mini-cart preview inline inside the toast: thumbnails, quantities, running total, a free-delivery progress banner, and a checkout button
- Every toast has a manual close button and auto-hides after 6 seconds (`toast.js`)

**Confirmation Modals** (triggered before destructive actions):
- **Delete Product Modal**: shown to superusers before deleting a product, from any page that shows a product card (a product with past orders is hidden rather than deleted)
- **Delete Contact Modal**: shown before removing a saved gift recipient from the Contacts tab

**Empty States**:
- **Empty Cart**: "Your cart is empty" with a Shop Now call to action
- **No Reviews**: "No reviews yet" / "Be the first to share your thoughts!" on the product detail page
- **No Orders**: "No orders found yet." on the profile's Orders tab
- **No Contacts**: "No contacts yet." on the profile's Contacts tab

**Real-Time Feedback**:
- AJAX quantity updates and removals in the cart, with totals and the free-delivery banner updating in place
- AJAX-paginated reviews on the product detail page (no full page reload)
- Interactive star-rating picker on the review form (click/hover to set 1-5 stars)
- The Stripe Payment Element mounts lazily, only once the payment section scrolls into view

**Form Validation Errors**:
- Django/crispy-forms field errors are shown inline, directly below the relevant input
- Required fields are marked, and Stripe's own card-input validation surfaces inline card errors at checkout

### Database Schema

The app uses Django's ORM, with SQLite in development and PostgreSQL in production.

#### Entity Relationship Diagram (ERD)

```
USER ||--o{ USERCUSTOMER : "linked via"
USERCUSTOMER }o--|| CUSTOMER : "resolves to"
CUSTOMER ||--o{ CONTACT : "has"
CUSTOMER |o--o{ ORDER : "places (guest orders have none)"
ORDER ||--o{ ORDERITEM : "contains"
PRODUCT ||--o{ ORDERITEM : "ordered as"
PRODUCT ||--o{ REVIEW : "receives"
ORDER |o--o{ REVIEW : "credits (optional)"
CONTACT |o--o{ ORDERITEM : "gifted to (optional)"
```
<p align="left">
  <a href="https://miro.com/app/live-embed/uXjVHU_iiV0=/?embedMode=view_only_without_ui&moveToViewport=-488%2C-690%2C2990%2C1511&embedId=930774328073" target="_blank" rel="noopener noreferrer"><strong>Full ERD here</strong></a>
</p>
<p align="center">
  <img src="docs/images/ERD.png" alt="Milky ERD" style="width: 100%; max-width: 1000px; height: auto;"><br>
</p>

**ERD note:** a user account and its `Customer` profile are linked by a separate `UserCustomer` row (two foreign keys), not by a `OneToOneField`. Nothing in the database stops a user having more than one `Customer`, but the code always reads the link with `.filter(user=request.user).first()`, so in practice it behaves as one-to-one.

**Legend (crow's-foot notation):** the two symbols next to each entity read as (minimum, maximum) participation.
- `||` one and only one
- `|o` zero or one (optional foreign key)
- `o{` zero or many
- `{` / `}` is the "crow's foot" (many). `--` is the relationship line
- **PK**: Primary Key
- **FK**: Foreign Key

Example: `USER ||--o{ USERCUSTOMER` means each `USERCUSTOMER` belongs to exactly one `USER`, and a `USER` has zero or many `USERCUSTOMER` rows.

---

#### Core Models & Relationships

**1. User (Django's built-in auth model)**
- **Purpose:** authentication and session identity
- **Key fields:** `id`, `username`, `email`, `password` (hashed), `is_active`, `is_staff`, `date_joined`

---

**2. `accounts.UserCustomer`**: join table between `User` and `Customer`
- **Foreign Keys:**
  - `user` (to `auth.User`, `CASCADE`): the login account
  - `customer` (to `Customer`, `CASCADE`): the profile that account owns
- **Fields:** just `id` and the two foreign keys
- **Constraint:** none. The `(user, customer)` pair is not made unique, so the schema would allow two rows for the same user. The app relies on `.filter(user=...).first()` to treat the link as 1:1.

---

**3. `accounts.Customer`**
- **Purpose:** the human profile behind an order, not tied 1:1 at the DB level, resolved via `UserCustomer`
- **Fields (all optional, the profile is filled in gradually):**
  - `name`, `surname` (CharField(255), blank)
  - `phone_number` (CharField(20), blank)
  - `address`, `city` (CharField(255), blank)
  - `county` (CharField(100), null/blank)
  - `postal_code` (CharField(20), blank)
  - `country` (CountryField via `django-countries`, null/blank)

---

**4. `accounts.Contact`**: a saved gift recipient ("friend")
- **Foreign Key:** `customer` (to `Customer`, `CASCADE`): the account that saved this recipient. Deleting the customer deletes their contacts
- **Fields:** `name`, `surname` (CharField(255), required), `phone_number` (CharField(20), required), `email` (EmailField, required)
- **Address (all required except `county`):** `address`, `city` (CharField(255)), `county` (CharField(100), null/blank), `postal_code` (CharField(20)), `country` (CountryField)
- `ip_address` (GenericIPAddressField, captured server-side at creation)
- **Note:** unlike `Customer`, a `Contact`'s address is required. It is created at the moment of an actual gift, not built up gradually.

---

**5. `products.Product`**
- **Fields:**
  - `sku` (CharField(255))
  - `name` (CharField(255), required)
  - `flavor` (CharField(50), null/blank, choices: chocolate, vanilla, fruity, caramel, nutty, special)
  - `description` (TextField, soft cap 500 chars)
  - `price` (DecimalField, 6 digits / 2 decimal places)
  - `product_image` (ImageField, null/blank): the single image used in the cart, checkout and order confirmation
  - `product_image_url` (URLField, null/blank): optional external image link, used for the cart image only when nothing is uploaded to `product_image`
  - `background_image`, `objects_image`, `can_image` (ImageField, null/blank): the layered storefront card. `background_image` is the base, the other two are optional overlays
  - `stock` (PositiveIntegerField, nullable)
  - `is_available` (BooleanField, default `True`)
  - `featured` (BooleanField, default `False`): shown on the home page
  - `display_order` (PositiveIntegerField, default `0`)
- **Constraint:** `sku` is unique. If left blank it is auto-filled by `generate_sku()` as `MILK-` plus 6 hex characters
- **Meta:** ordered by `display_order`, then `name`

---

**6. `products.Review`**
- **Foreign Keys:**
  - `product` (to `Product`, `CASCADE`, `related_name="reviews"`): the product being reviewed. Deleting the product deletes its reviews
  - `order` (to `checkout.Order`, `SET_NULL`, optional): links a review to the order that "earned" it, used to resolve the reviewer's account, and kept even if that order is later deleted
- **Fields:** `name`, `surname` (CharField(255), required), `rating` (PositiveIntegerField), `comment` (TextField(500), blank/null)
- **Constraint:** `rating` must be 1-5 (`MinValueValidator(1)` / `MaxValueValidator(5)`)
- No `Meta` ordering. The product page lists them newest-first via `order_by("-id")`

---

**7. `checkout.Order`**
- **Foreign Key:** `customer` (to `accounts.Customer`, `SET_NULL`, nullable): the account that placed the order. Null for guest checkouts, and kept null if the customer is later deleted
- **Fields:**
  - `reference_code` (CharField(100))
  - `stripe_pid` (CharField(254), nullable)
  - `status` (IntegerField, choices: 0 Pending / 1 Completed / 2 Cancelled)
  - `created_at` (DateTimeField, auto)
  - `order_total` (DecimalField): sum of its items, recalculated automatically whenever an item is saved
  - `delivery_cost` (DecimalField, default `0.00`): recalculated on every save (free from $25, otherwise $3.99)
  - `promo_discount_percent` (DecimalField, nullable): set when the order includes a gift
  - Separate `delivery_*` (mostly required, `county` and `postcode` optional) and `invoice_*` (optional) address blocks, plus `email` (required)
- **Constraint:** `reference_code` is unique and non-editable, auto-generated by `generate_reference_code()` as `ORDER-` plus 8 hex characters
- **Computed:** `grand_total` property = `order_total + delivery_cost`, minus the promo discount if set

---

**8. `checkout.OrderItem`**
- **Foreign Keys:**
  - `order` (to `Order`, `CASCADE`, `related_name="items"`): the order this line belongs to. Deleting the order deletes its items
  - `product` (to `Product`, `PROTECT`): the product bought on this line. A product that has been ordered can't be hard-deleted (the delete button hides it instead)
  - `gift_contact` (to `accounts.Contact`, `SET_NULL`, optional): set only on the single gift line, points to the friend who is notified by email
- **Fields:** `sku`, `unit_price` (snapshotted from the product at purchase time), `quantity`, `total_price` (auto-computed), `is_gift` (BooleanField, default `False`), `gift_message` (TextField, blank)
- **Side effect:** saving an `OrderItem` also recalculates and re-saves its parent `Order`'s `order_total`

---

#### Relationships Summary

<div align="center">

| Relationship | Models involved | Type | Enforcement |
|---|---|---|---|
| User / Customer | User, UserCustomer, Customer | Effectively One-to-One | Join model, app-enforced only |
| Customer to Contact | Customer, Contact | One-to-Many | `ForeignKey` + `CASCADE` |
| Customer to Order | Customer, Order | One-to-Many, optional | `ForeignKey` + `SET_NULL` |
| Order to OrderItem | Order, OrderItem | One-to-Many | `ForeignKey` + `CASCADE` |
| Product to OrderItem | Product, OrderItem | One-to-Many | `ForeignKey` + `PROTECT` |
| Product to Review | Product, Review | One-to-Many | `ForeignKey` + `CASCADE` |
| Order to Review | Order, Review | One-to-Many, optional | `ForeignKey` + `SET_NULL` |
| Contact to OrderItem | Contact, OrderItem | One-to-Many, optional | `ForeignKey` + `SET_NULL` |

</div>

---

#### Data Flow Examples

**Example 1: First checkout**
1. A signed-in user with no `Customer` yet reaches checkout.
2. A blank `Customer` and its `UserCustomer` link are created automatically.
3. The delivery form is saved back onto that `Customer` if "Save this delivery info to my profile" is checked.

**Example 2: Gift a Can**
1. The user picks a product and a recipient (existing `Contact`, or creates a new one) on the Gift a Can page.
2. The selection (product, recipient, message) is held in `request.session['gift']`, so no order exists yet. A brand-new `Contact`, if one is entered rather than picked, is saved at this point.
3. On successful payment, an `OrderItem` is created with `is_gift=True` and `gift_contact` set, and a gift confirmation email is sent to the recipient.

**Example 3: Order creation has two paths**
1. The browser is redirected back from Stripe to `checkout_success`, which creates the `Order` and its `OrderItem`s directly. This is the happy path.
2. Independently, Stripe's `payment_intent.succeeded` webhook creates the same order from the PaymentIntent's metadata **if it doesn't already exist** (looked up by `stripe_pid`). This is the reliability fallback, and it's also the only path that actually sends the confirmation and gift emails.

#### Schema Characteristics

<div align="center">

| Characteristic | Implementation | Benefit |
|---|---|---|
| Single database, ORM only | Django ORM and migrations, no raw SQL | Portable from SQLite (dev) to PostgreSQL (prod) |
| Explicit join model | `UserCustomer` links `User` and `Customer` instead of a `OneToOneField` | 1:1 in code, not constrained in the schema |
| Deliberate `on_delete` | `CASCADE` for owned rows (order items, contacts, reviews), `SET_NULL` for `Order.customer`, `Review.order` and `OrderItem.gift_contact`, `PROTECT` for `OrderItem.product` | Related rows are cleaned up without destroying order history, and deleting an ordered product is caught and turned into a hide (`is_available` off) |
| Unique constraints | `Product.sku` and `Order.reference_code`, both auto-generated | No duplicate SKUs or order references |
| Validated range | `Review.rating` bounded 1-5 by `MinValueValidator` / `MaxValueValidator` | Ratings can't go out of range |
| Choice fields | `Product.flavor` (6 choices), `Order.status` (Pending / Completed / Cancelled) | Data validation, powers admin filtering |
| Decimal money | `DecimalField` on every price and total, never a float | Exact currency arithmetic |
| Snapshotted line items | `OrderItem` copies `sku` and `unit_price` at checkout | Product edits never rewrite past orders (and an ordered product can't be hard-deleted, `PROTECT` blocks it) |
| Denormalised totals | `order_total` / `delivery_cost` stored on `Order`, resynced by `save()` overrides on `Order` and `OrderItem` | Totals ready for templates and admin without recomputing |
| Timestamp | `Order.created_at` (`auto_now_add`) | Order list sorts newest-first |
| Session-only transient state | Cart and in-progress gift selection live in `request.session` | The cart and gift selection never become database rows on their own |

</div>

## Features

### Existing Features

#### **Header & Navigation**

Responsive navigation for guests and authenticated users.

<p align="center"><strong>Public navigation</strong></p>
<p align="center">
  <img src="docs/images/public-nav.png" alt="Milky public navigation bar" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Authenticated navigation</strong></p>
<p align="center">
  <img src="docs/images/auth-nav.png" alt="Milky authenticated navigation bar" style="width: 90%; max-width: 1100px; height: auto;">
</p>

On mobile, the navigation collapses into a toggle menu that closes when you click outside it.

#### **Home Page**

Hero section, featured products, and a playful brand-first storefront experience.

<p align="center"><strong>Hero section</strong></p>
<p align="center">
  <img src="docs/images/hero.png" alt="Milky home page hero section" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Featured products</strong></p>
<p align="center">
  <img src="docs/images/our-favorites.png" alt="Milky featured product grid" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Superuser controls</strong></p>
<p align="center">
  <img src="docs/images/superuser-products.png" alt="Milky superuser product controls" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Benefits section</strong></p>
<p align="center">
  <img src="docs/images/good-for-you.png" alt="Milky benefits section" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Lifestyle section</strong></p>
<p align="center">
  <img src="docs/images/moments.png" alt="Milky lifestyle section" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **All Products**

Full product grid with the same storefront styling and superuser controls as the home page.

<p align="center"><strong>All products catalogue</strong></p>
<p align="center">
  <img src="docs/images/all-product.png" alt="All products page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Product Detail Page**

Product storytelling, nutrition info, reviews, and the purchase flow in one place.

<p align="center"><strong>Product detail</strong></p>
<p align="center">
  <img src="docs/images/products-details.png" alt="Product detail page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Customer reviews</strong></p>
<p align="center">
  <img src="docs/images/reviews.png" alt="Product review section" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Gift a Can**

A lightweight gifting flow designed for guest education and logged-in conversion.

<p align="center"><strong>Guest page</strong></p>
<p align="center">
  <img src="docs/images/gift-logout.png" alt="Gift a Can logged-out page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Logged-in customer</strong></p>
<p align="center">
  <img src="docs/images/gift-login.png" alt="Gift a Can logged-in form" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>One gift per order</strong></p>
<p align="center">
  <img src="docs/images/one-gift.png" alt="Gift a Can one-gift state" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Recipient email with confirmation sent to the friend</strong></p>
<p align="center">
  <img src="docs/images/gift-email.png" alt="Gift email preview" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Cart**

Session-based cart with live totals, delivery progress, and quick quantity updates.

<p align="center"><strong>Cart with items</strong></p>
<p align="center">
  <img src="docs/images/cart-1.png" alt="Cart page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Empty cart</strong></p>
<p align="center">
  <img src="docs/images/empty-cart.png" alt="Empty cart state" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Checkout Page**

Secure Stripe checkout with delivery, invoice, and payment details in a clear step-based flow.

<p align="center"><strong>Detail and Delivery </strong></p>
<p align="center">
  <img src="docs/images/checkout.png" alt="Checkout page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Stripe payment section</strong></p>
<p align="center">
  <img src="docs/images/payment.png" alt="Stripe payment section" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Order Confirmation**

Order confirmation and receipt follow-up built to feel clear and premium after purchase.

<p align="center"><strong>Order confirmation page</strong></p>
<p align="center">
  <img src="docs/images/order-confirmation.png" alt="Order confirmation page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Order confirmation email</strong></p>
<p align="center">
  <img src="docs/images/email-order-confirmation.png" alt="Order confirmation email" style="width: 50%; max-width: 700px; height: auto;">
</p>

#### **Profile Page**

A personal account area for saved details, orders, and gift contacts.

<p align="center"><strong>Profile overview</strong></p>
<p align="center">
  <img src="docs/images/profile.png" alt="Profile page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Order history</strong></p>
<p align="center">
  <img src="docs/images/profile-order.png" alt="Profile orders tab" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Saved contacts</strong></p>
<p align="center">
  <img src="docs/images/profile-contact.png" alt="Profile contacts tab" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Products Management (Superuser Only)**

Product creation and editing tools designed for lightweight storefront administration.

<p align="center"><strong>Add product form</strong></p>
<p align="center">
  <img src="docs/images/add-product.png" alt="Superuser products management" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Edit product form</strong></p>
<p align="center">
  <img src="docs/images/edit-product.png" alt="Superuser edit product form" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Authentication Pages** (django-allauth)

A consistent auth layout with clear form states for sign in, signup, reset, and change flows.

<p align="center"><strong>Register</strong></p>
<p align="center">
  <img src="docs/images/register.png" alt="Register page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Sign in</strong></p>
<p align="center">
  <img src="docs/images/sign-in.png" alt="Sign in page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Sign out</strong></p>
<p align="center">
  <img src="docs/images/sign-out.png" alt="Sign out page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Password reset</strong></p>
<p align="center">
  <img src="docs/images/password-reset.png" alt="Password reset page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Password change</strong></p>
<p align="center">
  <img src="docs/images/change-password.png" alt="Password change page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Footer**

- Social media links (X, Instagram, Facebook), each with an accessible label
- Copyright notice
- Consistent across every page

<p align="center">
  <img src="docs/images/footer.png" alt="Website footer" style="width: 90%; max-width: 1100px; height: auto;">
</p>

#### **Toast Notification System**

Fast visual feedback for cart actions, validation, warnings, and informational states.

<p align="center"><strong>Success toast</strong></p>
<p align="center">
  <img src="docs/images/success-toast.png" alt="Success toast" style="width: 60%; max-width: 700px; height: auto;">
</p>

<p align="center"><strong>Error toast</strong></p>
<p align="center">
  <img src="docs/images/error-toast.png" alt="Error toast" style="width: 60%; max-width: 700px; height: auto;">
</p>

<p align="center"><strong>Warning toast</strong></p>
<p align="center">
  <img src="docs/images/warning-toast.png" alt="Warning toast" style="width: 60%; max-width: 700px; height: auto;">
</p>

<p align="center"><strong>Info toast</strong></p>
<p align="center">
  <img src="docs/images/info-toast.png" alt="Info toast" style="width: 60%; max-width: 700px; height: auto;">
</p>

<p align="center"><strong>Cart toast preview</strong></p>
<p align="center">
  <img src="docs/images/cart-toast.png" alt="Cart toast preview" style="width: 60%; max-width: 700px; height: auto;">
</p>

#### **Modals**

Destructive actions are protected by confirmation modals to keep the experience clear and safe.

<p align="center"><strong>Delete product modal</strong></p>
<p align="center">
  <img src="docs/images/delete-product.png" alt="Delete product modal" style="width: 60%; max-width: 700px; height: auto;">
</p>

<p align="center"><strong>Delete contact modal</strong></p>
<p align="center">
  <img src="docs/images/delete-contact.png" alt="Delete contact modal" style="width: 60%; max-width: 700px; height: auto;">
</p>

#### **Input Fields & Forms**

- All forms render through `django-crispy-forms` with the `crispy-bootstrap5` pack, so fields, labels and help text share one style
- Field errors show inline, right under the field they belong to, and required fields are marked
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
- The cart summary and the product-page review list carry `aria-live="polite"` so their AJAX updates are read out
- Every page leads with a single `<h1>`, with no skipped heading levels
- Decorative images (backgrounds, commas, arrows) use an empty `alt`, and meaningful images carry a descriptive one
- Dark-brown text on the cream background keeps body copy well above the WCAG AA 4.5:1 ratio

#### **Base Templates**

- `templates/base.html` is the single site-wide shell: `<head>` (fonts, Bootstrap, Font Awesome, `base.css`), the header / navbar, `{% block content %}`, the footer, and the toast container
- Shared partials live in `templates/includes/`: `main_nav.html`, `mobile_nav.html`, the four toast variants, and `delete_product_modal.html`
- `django-allauth`'s pages extend a themed `templates/allauth/` layout so they match the rest of the site
- The custom error pages extend `templates/errors/base_error.html`

#### **Responsiveness**

- Mobile-first, with custom breakpoints at 768px, 1024px, 1440px, and 1800px, plus a small tweak below 360px
- Fluid typography via `clamp()` instead of hard jumps between breakpoints
- The checkout page reflows into a two-column layout with a sticky order summary from tablet width up
- The whole site is capped at a 1800px max content width and centred, so fixed elements (like the toast banner) align to the content edge, not the raw screen edge, on ultra-wide screens

## Error Pages

All four custom error pages share the same branded layout: a breakpoint-swapped illustration, the status code, a short title, a plain-language message, and a single "Back to Home" call to action.

The "Back to Home" button is the one clear way off the page, so a visitor who lands on a broken or forbidden URL gets straight back to the main page without touching the browser's back button. An automatic redirect was avoided on purpose, to keep the branded page and its screen-reader heading in place.

<div align="center">

| Error Code | Title Shown | Message Shown |
|---|---|---|
| **404** | Page Not Found | "The page you're looking for doesn't exist or has been moved." |
| **403** | Access Forbidden | "You don't have permission to access this page." |
| **405** | Method Not Allowed | "This request method is not supported for this page." |
| **500** | Server Error | "Something went wrong on our end. Please try again in a moment." |

</div>

<p align="center"><strong>Error 404</strong></p>
<p align="center">
  <img src="docs/images/error-404.png" alt="404 error page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Error 403</strong></p>
<p align="center">
  <img src="docs/images/error-403.png" alt="403 error page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Error 405</strong></p>
<p align="center">
  <img src="docs/images/error-405.png" alt="405 error page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

<p align="center"><strong>Error 500</strong></p>
<p align="center">
  <img src="docs/images/error-500.png" alt="500 error page" style="width: 90%; max-width: 1100px; height: auto;">
</p>

## Future Features

The following are planned for future releases, grouped by area:

**Shopping & Discovery**
- Product search, filtering, and sorting on the All Products page
- Wishlists: save a product for later without adding it to the cart
- Subscriptions: recurring delivery of a favourite flavour

**Checkout & Orders**
- Automatic stock management: decrement stock on purchase and block orders above the available quantity
- Discount / promo codes at checkout, beyond the automatic Gift a Can discount
- Order tracking and shipping notifications
- Guest order look-up: retrieve a past order without an account

**Gift a Can**
- Multiple gift recipients per order, instead of the current one-gift limit
- Shipping a gifted can to the recipient's own address: the address is already collected on the `Contact`, but the order still ships to the buyer, and one order cannot yet carry two delivery addresses

**Reviews**
- Editable and deletable reviews from the front end, for the reviewer
- Multiple photos per review

**Accounts & Engagement**
- Social login (Google / Facebook): `django-allauth` already supports it, no providers are configured yet
- Self-service account deletion
- A loyalty or rewards program
- Live chat support

## Technologies Used

Milky is built with **Django 6** and served with server-side-rendered templates
styled with **Bootstrap 5** for a responsive experience across mobile and
desktop. Data is stored in **PostgreSQL** in production (SQLite in local
development), and authentication is handled by **django-allauth** with email
login. Static files and product images are served from **AWS S3** via
django-storages. Payments run on **Stripe**, using a PaymentIntent and the
embedded Stripe Payment Element, with an order-confirming webhook as the source
of truth. Transactional email (order confirmations and gift notifications) is
sent over SMTP. The application is deployed on **Heroku** with Gunicorn.

### Languages

* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CSS](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Python Packages

Installed via `requirements.txt`:

<div align="center">

| Package | Purpose |
|---|---|
| [Django](https://www.djangoproject.com/) 6.0.4 | the web framework the whole project is built on |
| [django-allauth](https://docs.allauth.org/) | authentication, registration, and mandatory email verification |
| [django-crispy-forms](https://django-crispy-forms.readthedocs.io/) + [crispy-bootstrap5](https://pypi.org/project/crispy-bootstrap5/) | form rendering with the Bootstrap 5 template pack |
| [django-countries](https://pypi.org/project/django-countries/) | country fields on the delivery / invoice forms |
| [django-storages](https://django-storages.readthedocs.io/) + [boto3](https://pypi.org/project/boto3/) | static files and media on AWS S3 in production |
| [stripe](https://pypi.org/project/stripe/) | Stripe Python SDK, for the Payment Element and webhook handling |
| [dj-database-url](https://pypi.org/project/dj-database-url/) + [psycopg2](https://pypi.org/project/psycopg2/) | PostgreSQL connection in production |
| [gunicorn](https://pypi.org/project/gunicorn/) | WSGI server used on Heroku |
| [Pillow](https://pypi.org/project/pillow/) | image handling for uploaded product photos |

</div>

Dev / QA tooling: [flake8](https://pypi.org/project/flake8/) for Python linting.

### Frameworks, Libraries & Software

* [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/): responsive layout, utility classes, and the base for the crispy-forms template pack (loaded via CDN)
* [Font Awesome](https://fontawesome.com/): icons throughout the UI (loaded via CDN)
* [Google Fonts](https://fonts.google.com/): `Bebas Neue`, `Poppins`, and `Patrick Hand`
* [Blender](https://www.blender.org/): modelling the 3D can shown on the home page hero
* [Three.js](https://threejs.org/): renders and animates that 3D can model in the browser
* [ChatGPT](https://chatgpt.com/): generating the product can images and a flat texture map for the 3D can model
* [Adobe Photoshop](https://www.adobe.com/products/photoshop.html): building the layered product-card artwork, cutting out each element (background, floating objects, can) onto its own layer and positioning them individually, plus general photo editing
* [Claude](https://claude.ai/): checking spelling and wording in code comments and the README
* [Stripe](https://stripe.com/docs): checkout and payment processing
* [Heroku](https://www.heroku.com/): application hosting
* [AWS S3](https://aws.amazon.com/s3/): static file and media storage in production
* [GitHub](https://github.com/): version control and repository hosting
* [Figma](https://www.figma.com/): wireframes and high-fidelity design
* [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/): back-office management for products, reviews, and orders
* [W3C HTML Validator](https://validator.w3.org/): validating the rendered HTML of every page
* [W3C CSS Validator (Jigsaw)](https://jigsaw.w3.org/css-validator/): validating `static/css/base.css`
* [JSHint](https://jshint.com/): linting the scripts in `static/js/`
* [CI Python Linter](https://pep8ci.herokuapp.com/): checking the Python source for PEP 8 compliance
* [WAVE](https://wave.webaim.org/): accessibility evaluation of each page type
* [Lighthouse](https://developer.chrome.com/docs/lighthouse/): performance, accessibility, best-practices, and SEO audits

## Testing

Testing has two parts: an **automated test suite** for the back-end logic and access rules, and a **manual test plan** (the tables below) for the flows a script cannot judge well, UX, accessibility, responsive layout and the Stripe checkout.

Stripe runs in **test mode**, so checkout can be tested end to end without a real payment. Use card number `4242 4242 4242 4242` with any future expiry date, any 3-digit CVC and any postcode. More test cards are listed under [Deployment → Stripe](#stripe).

### Automated Tests

The suite lives in each app's `tests.py` and runs with `python manage.py test` (Django spins up a throwaway database, so real data is never touched). **43 tests, all passing.**

<div align="center">

| App | What it covers |
|---|---|
| `checkout` | delivery fee above / below / at the £25 free-delivery threshold, `grand_total` with and without the gift promo discount, `OrderItem.save()` keeping the line total and the parent order total in sync, unique reference codes, and that a signed-in user gets a 404 on another user's order confirmation |
| `products` | `generate_sku()` format and uniqueness, `single_image_url` fallback order, `Review.rating` rejected outside 1-5, the catalogue hiding unavailable products, `add`/`edit`/`delete` product refused to non-superusers, and an ordered product being hidden (not hard-deleted) |
| `cart` | adding / re-adding / updating / removing a session cart line, the 99-per-line cap, an unavailable product being refused, and the running totals from `cart_contents()` |
| `accounts` | the profile and contact views behind `@login_required`, a contact needing a completed profile first, and one user getting a 404 on another user's `edit-contact` / `delete-contact` URL |
| `home` | the landing page loading and its showcase listing only `featured` **and** available products |

**On the testing timeline:** the feature work was checked with the manual plan below as it was built. The automated suite was added near the end of the project, once the models and views had settled; from that point a test-first workflow was used for fixes and refinements.

### Authentication

<div align="center">

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Registration | Register with a new email and password | Account created, verification email sent (real email on Heroku, console in dev) | Pass |
| Duplicate Registration | Register with an email that already has an account | No new account. An "account already exists" email is sent, with no message confirming the address exists | Pass |
| Mandatory Email Verification | Try to sign in before verifying the email | Sign-in is blocked until the email is verified | Pass |
| Sign In | Sign in with valid credentials | User is authenticated and redirected | Pass |
| Invalid Sign In | Sign in with the wrong password | Error message shown, user stays on the sign-in page | Pass |
| Post-Login Redirect | Visit `/profile/` while logged out, then sign in | After sign-in the user lands on `/profile/` (via `?next=`) | Pass |
| Password Reset | Request a reset link for a registered email | Reset flow completes and the new password works | Pass |
| Password Reset - Unknown Email | Request a reset for an email with no account | Same generic confirmation message as for a valid email (no information leak) | Pass |
| Password Change | Change the password from the account while signed in | New password works, old one is rejected | Pass |
| Sign Out | Click Sign Out in the navbar | User is signed out and redirected | Pass |

</div>

### CRUD

<div align="center">

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Add Product (superuser) | Fill in the product form and submit | Product created and immediately visible in the catalogue | Pass |
| Add Product with no images (superuser) | Submit the product form leaving the image fields empty | Product is created. All Products and the home page show the no-image placeholder for it instead of erroring | Pass |
| Add Product with image URL only (superuser) | Fill in the Image URL field, leave the upload empty | Product is created. The linked image shows as the cart, checkout and confirmation thumbnail | Pass |
| Edit Product (superuser) | Change a product's fields and save | Changes reflected everywhere the product appears | Pass |
| Delete Product (superuser) | Confirm deletion of a product that has never been ordered | Product removed from the catalogue | Pass |
| Delete Ordered Product (superuser) | Delete a product that appears in a past order | The product is hidden from the shop (`is_available` off) instead of deleted. The past orders keep their line items, and a warning toast explains why | Pass |
| Add Review | Submit a star rating and comment on a product | Review appears in the paginated list | Pass |
| Add / Edit / Delete Contact | Manage a saved gift recipient from the Contacts tab | Contact list updates immediately, in place | Pass |
| Edit Profile Details | Change name, phone or address in the My Profile tab and save | Success toast, the new values persist on reload | Pass |
| Remove Gift from Cart | Add a Gift a Can, then remove it from the cart | The gift line disappears and the "one gift per order" slot is freed | Pass |
| Place Order | Complete checkout with a Stripe test card | Order created, confirmation page shown, order appears in Orders tab | Pass |

</div>

### Permissions

<div align="center">

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Products Management (non-superuser) | Visit `/products/add/` while signed in as a non-superuser | Redirected home with an error message | Pass |
| Products Management (logged out) | Visit `/products/add/` while logged out | Redirected to the sign-in page | Pass |
| Profile Access | Visit `/profile/` while logged out | Redirected to sign in | Pass |
| Own-Data Scoping | Sign in, then paste another account's order confirmation URL | 404. You only see your own orders | Pass |
| Guest Order Confirmation | Complete a guest checkout, then view the confirmation page | The page loads. A guest can only see the order they just placed, not another order's URL | Pass |
| Review While Logged Out | Open a product detail page while logged out | Review form is replaced by a "Sign In to leave a review" prompt | Pass |
| Gift a Can While Logged Out | Open `/products/gift/` while logged out | The promo page shows with "Login to gift" / "Register", not the gift form | Pass |
| Contact Ownership | While signed in as one user, paste another user's `delete-contact` / `edit-contact` URL | 404. The contact is neither shown nor deleted (scoped to its owner) | Pass |

</div>

### Forms

<div align="center">

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Checkout Validation | Submit the checkout form with required fields missing | Inline validation errors shown, submission blocked | Pass |
| Same as Delivery | Toggle the "same as delivery" checkbox at checkout | Invoice fields hide/show accordingly | Pass |
| Gift Form Validation | Submit the Gift a Can form without selecting a can | Submission blocked client-side, with a "Please choose a can" message under the picker | Pass |
| Gift to a Saved Contact | Send a gift, picking a saved contact instead of a new friend | The gift is added to the cart | Pass |
| Contact Form Validation | Submit the "Add a Friend" form with required fields missing | Inline errors shown, submission blocked | Pass |
| Registration Rules | Register with mismatched or too-weak passwords | allauth validation errors shown, account not created | Pass |

</div>

### UX

<div align="center">

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Cart Quantity Update | Use the +/- stepper on a cart line | Quantity and totals update in place via AJAX, no reload | Pass |
| Toast Feedback | Add a product to the cart | Success toast appears with a live mini-cart preview | Pass |
| Delete Confirmation | Click delete on a product (superuser) or a contact | Confirmation modal appears before anything is removed | Pass |
| Review Pagination | Page through a product's reviews | Review list swaps via AJAX without a full reload | Pass |
| Free-Delivery Banner | Change the cart total above and below the threshold | The progress banner updates live to match | Pass |
| Unavailable Product | Turn off a product's `is_available`, then check the catalogue and open its detail page directly | It no longer appears on All Products or the home page. Its detail page shows a disabled "Currently Unavailable" button | Pass |
| Zero-Stock Product | Open a product with `stock` at 0 | Add to Cart is replaced by a disabled "Out of Stock" button | Pass |
| Product card with partial layers | View a product with only a card background, and one with background + can | The card renders with whatever layers are present. Hovering moves the layers that exist and throws no JS error | Pass |
| Superuser overlay on any product | Open the detail page of a product with no card artwork, as a superuser | The Edit / Delete overlay is still shown | Pass |
| Mobile Nav Dismiss | Open the mobile menu, then click outside it or open the account dropdown | The menu closes | Pass |
| Gift Locked State | Open Gift a Can with a gift already in the cart | A page explains a gift is already in the cart, instead of the form | Pass |
| Empty States | View the cart, a product with no reviews, and the Orders / Contacts tabs while empty | Each shows its dedicated empty-state message | Pass |

</div>

### Accessibility

<div align="center">

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Keyboard navigation | Tab through the navbar, a product card, and the checkout form | Every interactive element is reachable and shows a visible focus state | Pass on Chrome, Edge and Firefox. Safari needs its "Press Tab to highlight each item" setting, which is off by default |
| Screen reader, toasts | Trigger a success and an error toast with a screen reader running | Both are announced through their `aria-live` region | Pass |
| Image alternatives | Inspect every `<img>` | Meaningful images have descriptive `alt`, decorative ones an empty `alt` | Pass |
| External links | Click the footer social links (X, Instagram, Facebook) | Each opens in a new tab (`target="_blank" rel="noopener"`) and its accessible name says "opens in a new tab". These are the only links that leave the site | Pass |
| Heading order | Run an outline check on each page type | One `<h1>` per page, no skipped levels | Pass |
| Colour contrast | Check brown-on-cream and brown-on-gold in a contrast checker | Meets WCAG AA for body text and buttons | Pass (roughly 9.8:1 on cream, 7.6:1 on the gold buttons) |
| WAVE | Run [WAVE](https://wave.webaim.org/) on each page type | No errors. Contrast and ARIA warnings reviewed | Pass |

</div>

### Validator Testing

<div align="center">

| Tool | Target | Result |
|------|--------|--------|
| [W3C HTML Validator](https://validator.w3.org/) | Each rendered page (validated from view-source) | Pass |
| [W3C CSS Validator (Jigsaw)](https://jigsaw.w3.org/css-validator/) | `static/css/base.css` | Pass (0 errors, 17 warnings, all expected) |
| [JSHint](https://jshint.com/) | Every file in `static/js/` (11 files) | Pass (0 warnings, 0 errors) |
| [flake8](https://flake8.pycqa.org/) | Python source (79-char lines, config in `setup.cfg`) | Pass (0 errors) |

</div>

<details>
<summary>HTML validation</summary>

<p align="center">
  <img src="docs/testing/html-validation.png" alt="W3C HTML validator results" style="width: 90%; max-width: 900px; height: auto;">
</p>
</details>

<details>
<summary>CSS validation</summary>

`static/css/base.css` passes the [W3C Jigsaw validator](https://jigsaw.w3.org/css-validator/) with **0 errors**.

<p align="center">
  <img src="docs/testing/css-validation.png" alt="W3C CSS validator results, no errors" style="width: 90%; max-width: 900px; height: auto;">
</p>

The 17 warnings are all expected and need no change:

<div align="center">

| Warning | Count | Reason |
|---|---|---|
| Imported style sheet not checked | 1 | Jigsaw does not follow the `@import` for the Patrick Hand font |
| CSS variables not statically checked | 10 | Jigsaw does not resolve `var(--token)` values, which is normal for a design-token-based stylesheet |
| `-webkit-appearance` / `::-webkit-*-spin-button` vendor extensions | 4 | Deliberate, to normalise the quantity number input across browsers |
| `auto` not defined for `pointer-events` | 2 | `pointer-events: auto` is valid per the CSS spec and widely supported. Jigsaw's data is out of date |
| `clip` is deprecated | 1 | Used in the visually-hidden pattern that hides a label while keeping it in the accessibility tree. `clip` stays the most cross-browser-compatible option |

</div>

<p align="center">
  <img src="docs/testing/css-warning.png" alt="W3C CSS validator warnings" style="width: 90%; max-width: 900px; height: auto;">
</p>
</details>

<details>
<summary>JavaScript validation</summary>

Every file in `static/js/` was run through [JSHint](https://jshint.com/) and passes with **0 warnings and 0 errors**. Each file carries a `/* jshint esversion: 6 */` directive at the top (`esversion: 8` for `checkout.js`, which uses `async`/`await`), plus `/* global bootstrap */` or `/* global Stripe */` where those library globals are used.

<div align="center">

| File | Result |
|------|--------|
| `add-review.js` | <img src="docs/testing/jshint-add-review.png" alt="JSHint results for add-review.js, no warnings" width="600"> |
| `admin-invoice.js` | <img src="docs/testing/jshint-admin.png" alt="JSHint results for admin-invoice.js, no warnings" width="600"> |
| `can-3d.js` | <img src="docs/testing/3d-can.png" alt="JSHint results for can-3d.js, no warnings" width="600"> |
| `cart.js` | <img src="docs/testing/jshint-cart.png" alt="JSHint results for cart.js, no warnings" width="600"> |
| `checkout.js` | <img src="docs/testing/jshint-checkout.png" alt="JSHint results for checkout.js, no warnings" width="600"> |
| `country-field.js` | <img src="docs/testing/jshint-countryfield.png" alt="JSHint results for country-field.js, no warnings" width="600"> |
| `gift-page.js` | <img src="docs/testing/gift-page.png" alt="JSHint results for gift-page.js, no warnings" width="600"> |
| `main.js` | <img src="docs/testing/jshint-main.png" alt="JSHint results for main.js, no warnings" width="600"> |
| `product-detail.js` | <img src="docs/testing/jshint-product-detail.png" alt="JSHint results for product-detail.js, no warnings" width="600"> |
| `profile.js` | <img src="docs/testing/jshint-profile.png" alt="JSHint results for profile.js, no warnings" width="600"> |
| `toast.js` | <img src="docs/testing/jshint-toast.png" alt="JSHint results for toast.js, no warnings" width="600"> |

</div>
</details>

<details>
<summary>Python validation</summary>

All Python source passes [flake8](https://flake8.pycqa.org/) with 0 errors (79-char lines, config in `setup.cfg`). `env.py`, `.venv/`, `__pycache__/` and the auto-generated `migrations/` are excluded in `setup.cfg`.

<p align="center">
  <img src="docs/testing/python-flake8.png" alt="flake8 run with no errors" style="width: 90%; max-width: 900px; height: auto;">
</p>
</details>

### Browser Compatibility

<div align="center">

| Browser | Version | Result |
|---------|---------|--------|
| Chrome | 151 | Pass |
| Firefox | 152 | Pass |
| Safari | 26.6 | Pass |
| Edge | 152 | Pass |

</div>

### Responsive Design

<div align="center">

| Device Category | Screen Size | Test Result | Notes |
|----------------|-------------|-------------|-------|
| Mobile - Very Small | 320px × 568px | Pass | iPhone 5 / SE (1st gen). A small below-360px CSS tweak keeps text and buttons from clipping |
| Mobile - Small | 390px × 844px | Pass | |
| Tablet | 768px × 1024px | Pass | Checkout switches to its two-column layout here |
| Tablet/Small Desktop | 1024px × 900px | Pass | |
| Laptop | 1440px × 1000px | Pass | |
| Desktop - Large | 2560px × 1300px | Pass | Toast banner and body content stay aligned at the 1800px max content width |
| Desktop - 5K | 5120px × 2880px | Pass | Content stays capped and centred at the 1800px max width. Layout matches the 2560px case |

</div>

### Performance

Lighthouse (Chrome DevTools) was run on the deployed site, on mobile and desktop, for performance, accessibility, best practices, and SEO.

<div align="center">

| Page | Device | Performance | Accessibility | Best Practices | SEO |
|------|--------|-------------|---------------|----------------|-----|
| Home | Mobile | 68 | 100 | 100 | 100 |
| Home | Desktop | 81 | 100 | 100 | 100 |
| All Products | Mobile | 65 | 100 | 100 | 100 |
| All Products | Desktop | 90 | 100 | 100 | 100 |
| Product Detail | Mobile | 74 | 100 | 100 | 100 |
| Product Detail | Desktop | 70 | 100 | 100 | 100 |
| Cart | Mobile | 77 | 100 | 100 | 100 |
| Cart | Desktop | 91 | 100 | 100 | 100 |

</div>

<details>
<summary>Lighthouse reports</summary>

<p align="center"><strong>Home (mobile)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-home-mobile.png" alt="Lighthouse home page, mobile" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>Home (desktop)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-home-desktop.png" alt="Lighthouse home page, desktop" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>All Products (mobile)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-all-products-mobile.png" alt="Lighthouse All Products page, mobile" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>All Products (desktop)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-all-products-desktop.png" alt="Lighthouse All Products page, desktop" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>Product Detail (mobile)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-product-detail-mobile.png" alt="Lighthouse Product Detail page, mobile" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>Product Detail (desktop)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-product-detail-desktop.png" alt="Lighthouse Product Detail page, desktop" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>Cart (mobile)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-cart-mobile.png" alt="Lighthouse Cart page, mobile" style="width: 90%; max-width: 900px; height: auto;">
</p>

<p align="center"><strong>Cart (desktop)</strong></p>
<p align="center">
  <img src="docs/lighthouse/lighthouse-cart-desktop.png" alt="Lighthouse Cart page, desktop" style="width: 90%; max-width: 900px; height: auto;">
</p>
</details>

**Notes on the scores**

- **Accessibility (100) and SEO (100)** are full marks on every page.
- **Best Practices** started at 77 and reached 100 after three changes: adding `XFrameOptionsMiddleware` (clickjacking protection), enabling HSTS / `SECURE_SSL_REDIRECT` / secure cookies in production, and loading `stripe.js` only on the checkout page instead of site-wide (which removed a third-party cookie from every other page).
- **Performance** ranges from the mid-60s (mobile) to the low-90s (desktop) and is held back by deliberate design choices, not unoptimised code:
  - Bootstrap and Font Awesome load render-blocking CSS from a CDN.
  - The storefront is image-heavy by design (each product card is three layered images).
  - On the home page only, the Three.js 3D can in the hero (~600 KB) is the single largest asset and the main drag on the mobile score.
- Possible future improvements: subset and self-host Font Awesome, lazy-load Three.js after first paint, serve pre-minified CSS/JS, and set explicit `width`/`height` on images.

### Bugs Found, Fixed, and Unresolved

<div align="center">

| Bug | Status | Notes |
|-----|--------|-------|
| On screens wider than 1800px the toast messages stuck to the far right edge of the browser instead of lining up with the page content | Fixed | The toast wrapper was `w-100` on a `position: fixed` element, so its width resolved against the viewport, not the centred max-width body. Capped it at the site's max content width and centred it. |
| The home page could be scrolled sideways a little on mobile | Fixed | Two Bootstrap `.row`s sat directly in a `<section>` with no `.container`, so the rows' negative gutter margins bled past the viewport. Wrapping both rows in `.container` fixed it. |
| Opening the checkout page auto-scrolled the view down to the Stripe card fields | Fixed | The payment form carried an `autofocus`, which pulled the viewport to it as the Payment Element mounted. Removed the autofocus and reset the scroll position on load (`checkout/forms.py`, `static/js/checkout.js`). |
| The toast container blocked clicks on links and buttons across the whole page | Fixed | The wrapper is `position: fixed` and full-width, so it sat over the page even with no toast showing. Added `pointer-events: none` on the wrapper and `pointer-events: auto` on the toasts themselves. |
| After the move to Django 6, static and media files 404'd on Heroku | Fixed | Django 6 dropped `STATICFILES_STORAGE` / `DEFAULT_FILE_STORAGE`. The S3 backends now go in the new `STORAGES` dict, and `STATIC_ROOT` had to be set for `collectstatic` in the build. |
| A disabled "Add to Cart" button still let an unavailable product be added through a direct POST | Fixed | `add_to_cart` didn't re-check `is_available` server-side. Added the check so the add is rejected with an error message. |
| A product URL with a non-numeric id (e.g. `/products/abc/`) reached the view and raised a 500 | Fixed | The route used `<product_id>` with no converter changed to `<int:product_id>`. |
| Using the cart stepper to drop an item's quantity to 0 deleted the whole line | Fixed | Quantity is now clamped to a minimum of 1. Removal is only via the explicit remove button. |
| Sign In on the deployed site intermittently returned "CSRF verification failed" (403) | Fixed | Heroku forwards HTTPS requests to Django over HTTP, so Django expected an `http://` origin while the browser sent `https://`. Added `SECURE_PROXY_SSL_HEADER` and `CSRF_TRUSTED_ORIGINS` for the Heroku domain. |

</div>

No known unresolved bugs at this time.

### Testing User Stories

All user stories from [User Stories](#user-stories) are validated below against the features that fulfil them.

#### New Visitor Stories

<div align="center">

| User Story | How It's Fulfilled | Features / Pages Used |
|---|---|---|
| As a new visitor, I want to see the product range and understand the brand. | The home page opens with a hero and a featured-products showcase, all Products shows the full catalogue. | Home Page, All Products |
| As a new visitor, I want to view a product's description, nutritional information, and customer reviews. | The Product Detail Page shows all three, plus a paginated review list. | Product Detail Page |
| As a new visitor, I want to add products to my cart and check out as a guest. | The cart and checkout flows don't require an account, and a guest order is saved without a linked customer. | Cart, Checkout Page |
| As a new visitor, I want to create an account so my details are saved for next time. | Registration via django-allauth, with delivery details saved to the `Customer` profile on request. | Register, Checkout Page ("save this delivery info") |

</div>

#### Existing User Stories

<div align="center">

| User Story | How It's Fulfilled | Features / Pages Used |
|---|---|---|
| As an existing user, I want to sign in and see my checkout form pre-filled with my saved details. | The checkout view builds the form from the signed-in user's saved `Customer` record. | Checkout Page |
| As an existing user, I want to view my order history. | The profile's Orders tab lists past orders, linking to the reused confirmation template. | Profile Page, Orders tab |
| As an existing user, I want to save a friend as a contact for gifting. | The profile's Contacts tab supports full CRUD on saved gift recipients. | Profile Page Contacts tab, Gift a Can |
| As an existing user, I want to reset my password. | django-allauth's password reset flow. | Password Reset |
| As an existing user, I want to leave a star rating and comment on a product. | The review form on the Product Detail Page, restricted to authenticated users. | Product Detail Page |

</div>

#### All Users Stories

<div align="center">

| User Story | How It's Fulfilled | Features / Pages Used |
|---|---|---|
| As a user, I want clear confirmation before a destructive action. | Shared confirmation modals for product deletion and contact deletion. | Products Management, Profile Page Contacts tab |
| As a user, I want feedback after every action. | The toast notification system, plus inline form validation errors. | Site-wide |
| As a user, I want the site to work well across devices. | Fluid typography and four custom breakpoints (768 / 1024 / 1440 / 1800px), verified manually across mobile, tablet, laptop, and wide desktop. | Site-wide |

</div>

## Security

- **Secrets in environment variables:** `SECRET_KEY`, the three Stripe keys (`STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WH_SECRET`), the AWS credentials and the email credentials are all read from the environment, via a local, git-ignored `env.py` in development and Heroku config vars in production. Nothing sensitive is committed to the repo.
- **`DEBUG` is environment-driven:** `DEBUG = "DEVELOPMENT" in os.environ`, so it is off in production. `ALLOWED_HOSTS` is limited to localhost and the Heroku app domain.
- **CSRF protection:** Django's CSRF middleware is active and every server-rendered form includes `{% csrf_token %}`. The Stripe webhook is the only `@csrf_exempt` view, verified instead through the Stripe signature header (`STRIPE_WH_SECRET`).
- **Authentication & access control:** account-only views (profile, contacts, reviews) are gated with `@login_required`. Products Management additionally goes through a `superuser_required` decorator (`add_product` / `edit_product` / `delete_product`). Cart and checkout stay open to guests by design, but no cart action writes to the database. Order pages are scoped so a guest can only see the order tied to their own session (`session["last_order"]`), and a signed-in user only orders linked to their own `Customer`.
- **Mandatory email verification:** `ACCOUNT_EMAIL_VERIFICATION = "mandatory"`, so a new account cannot sign in until its email is confirmed.
- **Payment data:** card details are entered into Stripe's Payment Element (card fields rendered in a Stripe-controlled iframe) and never reach the Django server or database. Only the Stripe PaymentIntent id is stored on the order.
- **Passwords:** hashed with Django's default PBKDF2 hasher. The reset flow uses django-allauth's signed, time-limited email tokens.
- **HTTPS hardening (production):** with `DEBUG` off, Django enables `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` and a one-year HSTS policy (`SECURE_HSTS_SECONDS` / `INCLUDE_SUBDOMAINS` / `PRELOAD`), sends `X-Frame-Options: DENY` via `XFrameOptionsMiddleware` for clickjacking protection, and trusts Heroku's HTTPS termination through `SECURE_PROXY_SSL_HEADER`.

### Could be hardened

- `django-allauth`'s `socialaccount` app is installed with no providers configured.

## Deployment

The application is hosted on **Heroku**, with all static files and media stored on **AWS S3**, payments handled by **Stripe**, and transactional email sent through **Gmail**.

### Branching model

The repository uses two long-lived branches.

| Branch | Purpose | `settings.py` |
|---|---|---|
| `main` | Release branch. This is what Heroku deploys. | Production defaults. `DEBUG` off unless a `DEVELOPMENT` env var is set, HTTPS redirect / HSTS / secure cookies enabled, Gmail SMTP e-mail. |
| `develop` | Working branch. All feature work and fixes happen here first. | Developer defaults. `DEBUG` on unless `DEBUG=False` is set, a verbose console `LOGGING` config, console e-mail backend. |

`settings.py` is **genuinely different on each branch**, not switched at runtime. Work is done on `develop`, then merged into `main` for a release. When resolving that merge, each branch keeps its own `settings.py`, so `main` stays on the production config. The data store configuration stays in one place on each branch (the `DATABASES` block), and both branches read every secret from the environment.

`develop` also carries `milky/tests.py`, which pins its extra settings (the console logging config) so an accidental change is caught by `python manage.py test`.

### Heroku

The application was deployed to Heroku. The steps to deploy are as follows:

1. Log in to the [Heroku dashboard](https://dashboard.heroku.com/) and click **New → Create new app**.
2. Choose a unique app name and a region, then click **Create app**. Note the app's `<name>.herokuapp.com` URL.
3. On the **Resources** tab, search the Add-ons bar for **Heroku Postgres** and add the **Essential-0** plan (the smallest Postgres plan, since Heroku no longer offers a free tier). This sets a `DATABASE_URL` config var automatically. *(Any hosted PostgreSQL provider works. Set `DATABASE_URL` yourself if you use one.)*
4. Locally, install the database and server packages: `pip install dj-database-url psycopg2 gunicorn`, then `pip freeze > requirements.txt`.
5. In `milky/settings.py`, `import dj_database_url` and switch `DATABASES` to use PostgreSQL in production and SQLite in development:

   ```python
   if "DATABASE_URL" in os.environ:
       DATABASES = {
           "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
       }
   else:
       DATABASES = {
           "default": {
               "ENGINE": "django.db.backends.sqlite3",
               "NAME": BASE_DIR / "db.sqlite3",
           }
       }
   ```

6. Set `SECRET_KEY` and `DEBUG` to read from the environment:

   ```python
   SECRET_KEY = os.environ.get("SECRET_KEY")
   DEBUG = "DEVELOPMENT" in os.environ
   ```

7. Add the Heroku app's hostname (from step 2) to `ALLOWED_HOSTS`:

   ```python
   ALLOWED_HOSTS = ["milky-app-839f694f035d.herokuapp.com", "localhost", "127.0.0.1"]
   ```

8. Add a `Procfile` in the project root:

   ```
   web: gunicorn milky.wsgi:application
   ```

   The repo also pins the Python version with a `.python-version` file (`3.13.5`), which Heroku reads at build time.

9. In Heroku **Settings → Reveal Config Vars**, add:
   - `SECRET_KEY`: generate one with a [Django secret key generator](https://djecrety.ir/)
   - `DISABLE_COLLECTSTATIC` = `1` (temporary, remove it once AWS S3 is configured below)
10. Commit and push all of the above to GitHub.
11. On the **Deploy** tab, connect the GitHub repository, then either **Deploy Branch** manually or **Enable Automatic Deploys** for `main`.
12. Once the first build succeeds, open **More → Run console** and set up the database:
    - `python manage.py migrate`
    - `python manage.py createsuperuser`
13. Still in the console, load the sample catalogue if the database is empty:
    `python manage.py loaddata products/fixtures/products.json products/fixtures/reviews.json`

> **Note:** local (`localhost:8000/admin/`) and Heroku (`.../admin/`) use two separate databases, so an account or order created on one will not appear on the other.

### Amazon Web Services (AWS)

AWS S3 is used to store all static files and media. To configure it:

1. Log in to AWS and open the **S3** service. Click **Create bucket**.
2. Give the bucket a name (the project uses `milky-static`) and pick a region (`us-east-1`). Under **Object Ownership**, select **ACLs enabled** + **Bucket owner preferred**. Under **Block Public Access**, **uncheck** "Block all public access" and tick the acknowledgement box, then **Create bucket**.
3. Open the bucket → **Properties** → **Static website hosting** → **Edit** → **Enable** → **Host a static website**, with `index.html` as the index document and `error.html` as the error document. *(Optional: the app serves files from the REST endpoint `milky-static.s3.amazonaws.com`, not the website endpoint, so this step isn't strictly required.)*
4. **Permissions → CORS → Edit**, and paste:

   ```json
   [
       {
           "AllowedHeaders": ["Authorization"],
           "AllowedMethods": ["GET"],
           "AllowedOrigins": ["*"],
           "ExposeHeaders": []
       }
   ]
   ```

5. **Permissions → Bucket policy → Edit → Policy generator** (opens a new tab). Choose **S3 Bucket Policy**, set **Principal** to `*`, **Action** to `GetObject`, paste the bucket **ARN** (copied from the bucket policy page), click **Add Statement → Generate Policy**, and copy it back into the editor. Append `/*` to the `Resource` value before saving:

   ```json
   {
       "Version": "2012-10-17",
       "Id": "Policy...",
       "Statement": [
           {
               "Sid": "Stmt...",
               "Effect": "Allow",
               "Principal": "*",
               "Action": "s3:GetObject",
               "Resource": "arn:aws:s3:::milky-static/*"
           }
       ]
   }
   ```

6. **Permissions → Access control list (ACL) → Edit**: tick **List** under **Everyone (public access)**, acknowledge the warning, and save.
7. Go to **IAM → User groups → Create group** (e.g. `manage-milky`).
8. **IAM → Policies → Create policy → JSON tab → Actions → Import policy → AmazonS3FullAccess**. In the imported JSON, replace the single `Resource` value with an array of your bucket ARN twice, once plain and once with `/*`:

   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "Statement1",
               "Effect": "Allow",
               "Action": ["s3:*"],
               "Resource": [
                   "arn:aws:s3:::milky-static",
                   "arn:aws:s3:::milky-static/*"
               ]
           }
       ]
   }
   ```

   Name it (e.g. `milky-policy`), give it a description, and create it.
9. Attach that policy to the group: **User groups → (your group) → Permissions → Add permissions → Attach policies**.
10. **IAM → Users → Create user** (e.g. `milky-staticfiles-user`), add it to the group, and create it. Open the user → **Security credentials → Create access key → Application running outside AWS → Create access key**, then **Download .csv file** (the secret key is shown only once). In the CSV, the value **before** the comma is `AWS_ACCESS_KEY_ID`. Everything **after** the comma (any `/` included) is `AWS_SECRET_ACCESS_KEY`.
11. Locally, install the storage packages: `pip install boto3 django-storages`, then `pip freeze > requirements.txt`.
12. Add `"storages"` to `INSTALLED_APPS`, and add this block to `settings.py`:

    ```python
    if "USE_AWS" in os.environ:
        AWS_S3_OBJECT_PARAMETERS = {
            "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
            "CacheControl": "max-age=86400",
        }

        AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        AWS_STORAGE_BUCKET_NAME = "milky-static"
        AWS_REGION_NAME = "us-east-1"
        AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

        STATICFILES_LOCATION = "static"
        MEDIAFILES_LOCATION = "media"

        # Django 4.2+ storage config
        STORAGES = {
            "default": {"BACKEND": "custom_storages.MediaStorage"},
            "staticfiles": {"BACKEND": "custom_storages.StaticStorage"},
        }

        STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"
    ```

13. Create `custom_storages.py` in the project root:

    ```python
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage


    class StaticStorage(S3Boto3Storage):
        location = settings.STATICFILES_LOCATION


    class MediaStorage(S3Boto3Storage):
        location = settings.MEDIAFILES_LOCATION
    ```

14. In Heroku Config Vars, add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` from the CSV, add `USE_AWS` = `True`, and **remove** `DISABLE_COLLECTSTATIC`.
15. Commit and push to GitHub. On the next build, `collectstatic` uploads the static files to S3.
16. In the S3 bucket, create a `media/` folder and upload the product images, granting them public-read access.

### Stripe

1. Log in to [Stripe](https://dashboard.stripe.com/) and open **Developers → API keys**.
2. Copy the **Publishable key** and **Secret key** into Heroku Config Vars as `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY`.
3. Go to **Developers → Webhooks → Add endpoint**. Set the URL to `https://<your-app>.herokuapp.com/checkout/webhook/` and select all events, then add the endpoint.
4. Click **Reveal signing secret** and save it in Heroku Config Vars as `STRIPE_WH_SECRET`.

The deployed site keeps Stripe in **test mode**, so no real payment is ever taken.

**Test cards**

<div align="center">

| Card number | Result |
|---|---|
| `4242 4242 4242 4242` | Payment succeeds |
| `4000 0000 0000 9995` | Payment declined (insufficient funds) |
| `4000 0025 0000 3155` | Requires 3D Secure authentication |

</div>

For any test card, use **any future expiry date**, **any 3-digit CVC** and **any
postcode**. The full list is in the
[Stripe testing docs](https://docs.stripe.com/testing).

### Emails

`settings.py` uses the console email backend in development and Gmail SMTP in production:

```python
if "DEVELOPMENT" in os.environ:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "milky@example.com"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASS")
    DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")
```

1. Use a personal Gmail account (not a CI student account, which blocks SMTP sending).
2. Go to your [Google Account](https://myaccount.google.com/) → **Security**.
3. Turn on **2-Step Verification** (a phone number is required).
4. Search the Google Account for **App passwords**, give the app a name, and click **Create**. Copy the 16-character password.
5. Add Heroku Config Vars `EMAIL_HOST_USER` (the Gmail address) and `EMAIL_HOST_PASS` (the 16-character app password, no spaces).

### Forking & Cloning the Repository

**Fork**

1. On the [repository page](https://github.com/Carokyp/Milky), click **Fork** (top right).
2. GitHub creates a copy under your own account.

**Clone & run locally**

1. On the repo page, click the green **Code** button and copy the HTTPS URL.
2. In a terminal, navigate to where you want the project and run `git clone https://github.com/Carokyp/Milky.git`
3. `cd Milky`
4. Create and activate a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`
6. Create a git-ignored `env.py` in the project root:

   ```python
   import os

   os.environ["SECRET_KEY"] = "any-dev-secret-key"
   os.environ["DEVELOPMENT"] = "1"
   os.environ["STRIPE_PUBLIC_KEY"] = "pk_test_..."
   os.environ["STRIPE_SECRET_KEY"] = "sk_test_..."
   os.environ["STRIPE_WH_SECRET"] = "whsec_..."
   ```

7. Apply migrations: `python manage.py migrate`
8. Load the sample data: `python manage.py loaddata products/fixtures/products.json products/fixtures/reviews.json`
9. Create a superuser: `python manage.py createsuperuser`
10. Run the server: `python manage.py runserver`

## Credits

### Visual Design References

Drinks-brand storefronts and design concepts that informed Milky's playful, layered visual direction:

- [Johnny's Dirty Soda](https://www.johnnysdirtysoda.com/)
- [More Nutrition](https://more-nutrition.webflow.io/)
- [Drink Charlie's](https://www.drinkcharlies.com/#products)
- [SPYLT](https://www.spylt.com/)
- [Mana Yerba Mate](https://en.manayerbamate.com/)
- [Drinks E-commerce Web Design (Dribbble)](https://dribbble.com/shots/27172705-Drinks-E-commerce-Web-Design)
- [Drink PE E-Commerce Website (Dribbble)](https://dribbble.com/shots/26471668-Drink-PE-E-Commerce-Website)

### Media

<div align="center">

| Asset | Source |
|---|---|
| Product can images (the can layer on each product card) and the texture map on the 3D can model | Generated with [ChatGPT](https://chatgpt.com/) |
| Illustrations — lifestyle (`can-kitchen`, `gift-a-can`, `group-enjoying-drinks`), auth pages (`login`, `logout`, `register`, `forgot-password`, `verify-email`), error pages (`error-desktop`, `error-mobile`) | Generated with [ChatGPT](https://chatgpt.com/) |
| 3D can model on the home hero | Modelled by me in [Blender](https://www.blender.org/), rendered in the browser with [Three.js](https://threejs.org/) |
| Nutrition icons and decorative marks (in `static/images/`) | [Flaticon](https://www.flaticon.com/) — free licence, attribution required |
| UI icons (navbar, toasts, social links) | [Font Awesome](https://fontawesome.com/) |
| Backgrounds, gradients, the product-card "objects" layer, brand marks | Free stock imagery, assembled by me in [Adobe Photoshop](https://www.adobe.com/products/photoshop.html) (cut-outs, background removal, colour adjustment, layering) |
| Fonts | [Google Fonts](https://fonts.google.com/) — Bebas Neue, Poppins, Patrick Hand |

</div>

### Code References

This project incorporates code patterns and techniques from various sources, with modifications to fit the project's specific requirements. Below are the primary references used during development:

#### **Walkthrough Project**
- **Code Institute:** this project is based on Code Institute's walkthrough project **Boutique Ado**, "Building an E-Commerce Platform".

#### **Backend - Django**
- [Django Official Documentation](https://docs.djangoproject.com/): core framework, models, views, forms
- [django-allauth Documentation](https://docs.allauth.org/): authentication, registration, and email verification flows
- [Django ORM Relationships](https://docs.djangoproject.com/en/stable/topics/db/models/): ForeignKey/OneToOne relationships and cascade behavior
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/): custom `ModelAdmin` configuration, inlines, and `save_formset` overrides

#### **Payments**
- [Stripe Payment Element Documentation](https://stripe.com/docs/payments/payment-element): client-side integration
- [Stripe Webhooks Documentation](https://stripe.com/docs/webhooks): server-side payment confirmation and signature verification

#### **JavaScript**
- [Three.js Documentation](https://threejs.org/docs/): loading and animating the 3D can model
- [Intersection Observer API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API): lazy-mounting the Stripe Payment Element

#### **General References**
- [Stack Overflow](https://stackoverflow.com/): troubleshooting specific implementation issues
- [Mozilla Developer Network (MDN)](https://developer.mozilla.org/): web standards and API documentation
- [W3Schools](https://www.w3schools.com/): web development tutorials and reference

