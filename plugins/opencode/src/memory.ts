/** Pointer-tracked capture. Pure: no server, no processes, no filesystem. */

export interface HistoryItem {
  id: string;
  text: string;
}

export interface HookEvent {
  session_id: string;
  event: string;
  items: string[];
}

/** Items after the pointer. Unknown pointer means the whole history is the gap. */
export function unseenItems(
  history: HistoryItem[],
  pointer: string | null,
): { items: HistoryItem[]; pointer: string | null } {
  if (history.length === 0) return { items: [], pointer };
  if (pointer === null) return { items: [...history], pointer: pointerOf(history) };
  const at = history.findIndex((item) => item.id === pointer);
  if (at === -1) return { items: [...history], pointer: pointerOf(history) };
  const items = history.slice(at + 1);
  return { items, pointer: items.length > 0 ? items[items.length - 1].id : pointer };
}

function pointerOf(history: HistoryItem[]): string | null {
  return history.length > 0 ? history[history.length - 1].id : null;
}

/** First shell word, honoring single and double quotes. */
export function firstToken(command: string): string {
  let word = "";
  let quote = "";
  for (const char of command.trim()) {
    if (quote !== "") {
      if (char === quote) quote = "";
      else word += char;
    } else if (char === '"' || char === "'") {
      quote = char;
    } else if (char === " " || char === "\t") {
      if (word !== "") return word;
    } else {
      word += char;
    }
  }
  return word;
}

/** Payload for `mem-hook --host opencode`: items ride along, no transcript read. */
export function buildHookEvent(
  sessionID: string,
  event: string,
  items: HistoryItem[],
): HookEvent {
  return { session_id: sessionID, event, items: items.map((item) => item.text) };
}

/** Session history → archivable items. Message shapes vary by host version,
 *  so this walks defensively and skips what carries no text. */
export function toHistoryItems(messages: unknown[]): HistoryItem[] {
  const items: HistoryItem[] = [];
  messages.forEach((message, index) => {
    if (typeof message !== "object" || message === null) return;
    const record = message as Record<string, unknown>;
    const id = String(record["messageID"] ?? record["id"] ?? `msg-${index}`);
    const role = String(record["role"] ?? record["type"] ?? "message");
    const direct = record["text"] ?? record["content"];
    const found = typeof direct === "string" ? [direct] : collectText(record);
    const text = found.join("\n").trim();
    if (text !== "") items.push({ id, text: `${role}: ${text}` });
  });
  return items;
}

function collectText(value: unknown): string[] {
  if (typeof value === "string") return [];
  if (Array.isArray(value)) return value.flatMap(collectText);
  if (typeof value === "object" && value !== null) {
    const record = value as Record<string, unknown>;
    if (record["type"] === "text" && typeof record["text"] === "string") {
      return [record["text"]];
    }
    return Object.values(record).flatMap(collectText);
  }
  return [];
}
