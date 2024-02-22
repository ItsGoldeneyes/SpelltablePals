export function envsure(env: string) {
  const value = Deno.env.get(env);
  if (Deno.env.has(env) === false || value === undefined) {
    console.error(`Environment variable ${env} is not set`);
    Deno.exit(1);
  }
  return value;
}
