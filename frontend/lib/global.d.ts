import { Database } from "./database.types";

declare global {
    type Job = Database["public"]["Tables"]["jobs"]["Row"];
}
