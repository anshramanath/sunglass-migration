-- ============================================================
-- 001_initial_schema.sql
-- Initial schema for bikershades multi-brand platform
-- ============================================================

create table brands (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  slug text not null unique
);

create table categories (
  id uuid primary key default gen_random_uuid(),
  brand_id uuid not null references brands(id),
  parent_id uuid references categories(id),
  name text not null,
  slug text not null
);

create table products (
  id uuid primary key default gen_random_uuid(),
  brand_id uuid not null references brands(id),
  name text not null,
  slug text not null,
  sku text not null unique,
  wp_url text,
  product_url text,
  description text,
  summary text[],
  attributes jsonb,
  sale boolean not null default false,
  min_price_cents int not null,
  max_price_cents int not null,
  sale_price_cents int,
  average_rating float not null default 0,
  review_count int not null default 0,
  stock int not null default 1,
  weight float,
  weight_unit text not null default 'oz',
  length float,
  width float,
  height float,
  dimension_unit text not null default 'in'
);

create table product_categories (
  product_id uuid not null references products(id),
  category_id uuid not null references categories(id),
  primary key (product_id, category_id)
);

create table variations (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references products(id),
  slug text not null,
  sku text not null unique,
  variation text[],
  wp_url text,
  product_url text,
  description text,
  sale boolean not null default false,
  regular_price_cents int not null,
  sale_price_cents int not null,
  stock int not null default 1,
  weight float,
  weight_unit text not null default 'oz',
  length float,
  width float,
  height float,
  dimension_unit text not null default 'in',
  image_src text,
  image_name text
);

create table product_images (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references products(id),
  src text not null,
  name text not null,
  sort_order int not null default 0
);

create table description_images (
  id uuid primary key default gen_random_uuid(),
  product_id uuid references products(id),
  variation_id uuid references variations(id),
  src text not null,
  name text not null,
  sort_order int not null default 0,
  check (
    (product_id is not null and variation_id is null) or
    (product_id is null and variation_id is not null)
  )
);

create table admins (
  user_id uuid primary key references auth.users(id)
);
