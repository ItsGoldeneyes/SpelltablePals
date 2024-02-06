import { BlockedUser } from "../src/mod.ts";
import { Handlers, PageProps } from "$fresh/server.ts";
import { fetchBlockList } from "../src/mod.ts";
import BlockListTable from "../components/BlockListTable.tsx";

export const handler: Handlers<BlockedUser[]> = {
  GET: async (_req, ctx) => {
    const blockedUsers = await fetchBlockList();
    return ctx.render(blockedUsers);
  },
};

export default function Home(props: PageProps<BlockedUser[]>) {
  const blockedUsers = props.data;
  return (
    <html>
      <body>
        <div>
          <BlockListTable
            blocked_users={blockedUsers}
            class="m-auto children:(w-[50%] children:(border border-gray-300 children:(px-4)))"
          />
        </div>
      </body>
    </html>
  );
}
