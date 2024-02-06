import { JSX } from "preact";
import { BlockedUser } from "../src/fetchList.ts";

type Props = {
  blocked_users: BlockedUser[];
} & JSX.HTMLAttributes<HTMLTableElement>;

export default function BlockListTable(
  props: Props,
) {
  const blockedUsers = props.blocked_users;
  return (
    <table {...props}>
      <tr>
        <th>Username</th>
        <th>Updated On</th>
        <th>Reason</th>
      </tr>
      {blockedUsers.sort((a, b) => b.changed_on - a.changed_on).map((user) => (
        <tr>
          <td>{user.username}</td>
          <td>{new Date(user.changed_on * 1000).toDateString()}</td>
          <td>{user.reason}</td>
        </tr>
      ))}
    </table>
  );
}
