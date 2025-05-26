import type { ReactNode } from "react";
import "../css/app.css";

type WrapperProps = {
  children: ReactNode;
};

export default function Wrapper(props: WrapperProps) {
  return props.children;
}
