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

-- Documentos: bucket privado no Storage, um arquivo criptografado por documento.
insert into storage.buckets (id, name, public, file_size_limit)
values ('vault-docs', 'vault-docs', false, 20971520)
on conflict (id) do update set public = false, file_size_limit = 20971520;

drop policy if exists "vault docs select" on storage.objects;
drop policy if exists "vault docs insert" on storage.objects;
drop policy if exists "vault docs update" on storage.objects;
drop policy if exists "vault docs delete" on storage.objects;

create policy "vault docs select" on storage.objects
  for select to authenticated
  using (bucket_id = 'vault-docs' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "vault docs insert" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'vault-docs' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "vault docs update" on storage.objects
  for update to authenticated
  using (bucket_id = 'vault-docs' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'vault-docs' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "vault docs delete" on storage.objects
  for delete to authenticated
  using (bucket_id = 'vault-docs' and (storage.foldername(name))[1] = auth.uid()::text);

