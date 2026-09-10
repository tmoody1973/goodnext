import { describe, expect, it } from "vitest";
import { telHref } from "./phone";

describe("telHref", () => {
  it("turns a directory phone number into a tel link", () => {
    expect(telHref("(414) 249-3866")).toBe("tel:4142493866");
    expect(telHref("1-800-362-3002")).toBe("tel:18003623002");
  });
  it("turns the three-digit 2-1-1 help line into tel:211", () => {
    expect(telHref("2-1-1")).toBe("tel:211");
  });
  it("leaves text and short numbers as text", () => {
    expect(telHref("no phone listed")).toBeNull();
    expect(telHref("123")).toBeNull();
  });
});
