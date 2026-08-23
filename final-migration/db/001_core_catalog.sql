-- ============================================================
-- 001_core_catalog.sql
-- Core catalog tables: brands, categories, products, images
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
  sort_order int not null,
  view_count int default null
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
  view_count int not null default 0,
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

create table admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);


create or replace function increment_category_view(p_id uuid, p_brand_slug text)
returns void language sql as $$
  update categories
  set view_count = coalesce(view_count, 0) + 1
  where id = p_id and brand_slug = p_brand_slug;
$$;

create or replace function increment_product_view(p_slug text, p_brand_slug text)
returns void language sql as $$
  update products
  set view_count = view_count + 1
  where slug = p_slug and brand_slug = p_brand_slug;
$$;
