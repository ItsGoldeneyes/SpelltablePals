import { FreshContext } from "$fresh/server.ts";
import { tldts } from "../deps.ts";

const invite = "https://discord.com/invite/9QwzXz5Rt5";

export function handler(
  req: Request,
  ctx: FreshContext,
) {
  const domain = tldts.parse(req.url);
  console.log(domain);
  if (domain.subdomain === "discord") {
    return Response.redirect(invite, 307);
  }
  return ctx.next();
}
