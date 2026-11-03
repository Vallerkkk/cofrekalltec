-- Cofre KallTec — execute este arquivo no SQL Editor do Supabase.
-- Guarda apenas o cofre já criptografado (AES-256-GCM) do usuário logado.

create table if not exists public.vault (
  user_id uuid primary key references auth.users(id) on delete cascade,
  envelope jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.vault enable row level security;

drop policy if exists "vault select own" on public.vault;
drop policy if exists "vault insert own" on public.vault;
drop policy if exists "vault update own" on public.vault;

create policy "vault select own" on public.vault
  for select to authenticated using (auth.uid() = user_id);

create policy "vault insert own" on public.vault
  for insert to authenticated with check (auth.uid() = user_id);

create policy "vault update own" on public.vault
  for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

revoke all on public.vault from anon;
