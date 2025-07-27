import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from "@/components/ui/dialog"
import JobForm from "./job-form"
import { useState } from "react";

export default function NewJobDialog() {
    const [open, setOpen] = useState(false);
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button variant="outline">New Job</Button>
            </DialogTrigger>
            <DialogContent className="max-h-11/12 overflow-y-scroll scrollbar-custom">
                <JobForm setOpen={setOpen} />
            </DialogContent>
        </Dialog>
  )
}
