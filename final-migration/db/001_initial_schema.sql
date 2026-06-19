-- ============================================================
-- 001_initial_schema.sql
-- Full schema for sunglass monster multi-brand platform
-- Includes: core catalog + user cart and bookmarks
-- ============================================================

create table brands (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  slug text not null unique
);

create table categories (
  id uuid primary key default gen_random_uuid(),
  brand_slug text not null references brands(slug) on delete cascade,
  parent_id uuid references categories(id) on delete cascade,
  name text not null,
  slug text not null,
  sort_order int not null
);

create table products (
  id uuid primary key default gen_random_uuid(),
  brand_slug text not null references brands(slug) on delete cascade,
  name text not null,
  slug text not null,
  sku text,
  description text not null,
  summary text[] not null,
  attributes jsonb not null,
  featured boolean not null,
  total_sales int,
  sale boolean not null,
  min_price_cents int not null,
  max_price_cents int not null,
  sale_price_cents int,
  unique (brand_slug, slug),
  unique (brand_slug, name)
);

create table product_categories (
  product_id uuid not null references products(id) on delete cascade,
  category_id uuid not null references categories(id) on delete cascade,
  primary key (product_id, category_id)
);

create table variations (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references products(id) on delete cascade,
  sku text not null,
  attribute jsonb not null,
  sale boolean not null,
  regular_price_cents int not null,
  sale_price_cents int,
  total_sales int not null
);

create table product_images (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references products(id) on delete cascade,
  src text not null,
  name text not null,
  sort_order int not null
);

create table variation_images (
  id uuid primary key default gen_random_uuid(),
  variation_id uuid not null references variations(id) on delete cascade,
  src text not null,
  name text not null,
  sort_order int not null
);

create table description_images (
  id uuid primary key default gen_random_uuid(),
  brand_slug text not null references brands(slug) on delete cascade,
  src text not null,
  name text not null,
  unique (brand_slug, src)
);

create table product_description_images (
  product_id uuid not null references products(id) on delete cascade,
  image_id uuid not null references description_images(id) on delete cascade,
  primary key (product_id, image_id)
);

create table orders (
  id                    uuid        primary key default gen_random_uuid(),
  user_id               uuid        references auth.users(id) on delete set null,
  brand_slug            text        not null references brands(slug) on delete cascade,
  stripe_session_id     text        not null unique,
  stripe_payment_intent text not null unique,
  status                text        not null default 'pending',
  total_cents           int         not null,
  shipping_address      jsonb       not null,
  created_at            timestamptz not null default now()
);

alter table orders enable row level security;
grant select on orders to authenticated;

create policy "orders: users read own rows"
  on orders for select
  using (auth.uid() = user_id);


create table order_items (
  id            uuid  primary key default gen_random_uuid(),
  order_id      uuid  not null references orders(id) on delete cascade,
  product_slug  text  not null,
  sku           text  not null,
  name          text  not null,
  image_src     text  not null,
  price_cents   int   not null,
  quantity      int   not null,
  attribute     jsonb not null default '[]'
);

alter table order_items enable row level security;
grant select on order_items to authenticated;

create policy "order_items: users read own rows"
  on order_items for select
  using (exists (
    select 1 from orders
    where orders.id = order_items.order_id
      and orders.user_id = auth.uid()
  ));


create table admins (
  user_id uuid primary key references auth.users(id)
);

create table cart_items (
  id            uuid        primary key default gen_random_uuid(),
  user_id       uuid        not null references auth.users(id) on delete cascade,
  brand_slug    text        not null references brands(slug) on delete cascade,
  product_slug  text        not null,
  sku           text        not null,
  attribute     jsonb       not null default '[]',
  name          text        not null,
  image_src     text        not null,
  price_cents   int         not null,
  quantity      int         not null default 1 check (quantity > 0),
  updated_at    timestamptz not null default now()
);

alter table cart_items enable row level security;
grant select, insert, update, delete on cart_items to authenticated;

create policy "cart_items: users manage own rows"
  on cart_items for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);


create table bookmarks (
  id            uuid        primary key default gen_random_uuid(),
  user_id       uuid        not null references auth.users(id) on delete cascade,
  brand_slug    text        not null references brands(slug) on delete cascade,
  product_slug  text        not null,
  name          text        not null,
  image_src     text        not null,
  created_at    timestamptz not null default now()
);

alter table bookmarks enable row level security;
grant select, insert, update, delete on bookmarks to authenticated;

create policy "bookmarks: users manage own rows"
  on bookmarks for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create function increment_variation_total_sales(p_variation_id uuid, p_qty int)
returns void
language sql
as $$
  update variations set total_sales = total_sales + p_qty where id = p_variation_id;
$$;

create function increment_product_total_sales(p_product_id uuid, p_qty int)
returns void
language sql
as $$
  update products set total_sales = coalesce(total_sales, 0) + p_qty where id = p_product_id;
$$;
