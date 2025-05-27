import type { PageContext } from "vike/types";
import type { CreateVideoData } from "./+data.shared";

export function title(pageContext: PageContext<CreateVideoData>) {
  return `Create Video with ${pageContext.data?.actor?.name}`;
}
