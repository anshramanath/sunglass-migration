-- ============================================================
-- 003_orders.sql
-- Adds orders and order_items tables
-- Users can read their own orders; writes are admin-only (webhook)
-- ============================================================

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
