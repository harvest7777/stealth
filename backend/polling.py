import modal
f = modal.Function.from_name("example-get-started", "supabase_function")
print(f.remote())