import JobList from "@/components/jobs/job-list"
import useWebSocket, { ReadyState } from "react-use-websocket";

import { useJobStore } from "@/stores/useJobsStore"
import { useEffect } from "react"
import NewJobDialog from "@/components/jobs/new-job-dialog";
import { BACKEND_DOMAIN } from "@/lib/config";
export default function ManageJobsPage() {
    const { setJobs, initialized, updateJob } = useJobStore()

    // IMPORTANT: may be ws:// or wss:// depending on if you use http or https
    // DO NOT use localhost, use direct IP 127.0.0.1 or the domain

    const { lastMessage, readyState } = useWebSocket(`ws://${BACKEND_DOMAIN}/ws`, {
        onOpen: () => console.log("✅ Connected to WebSocket"),
        onClose: () => console.log("❌ WebSocket closed"),
        onError: (event) => console.error("WebSocket error:", event),
        shouldReconnect: () => true, // Auto reconnect
    });

    // Track incoming messages
    useEffect(()=>{
        if (lastMessage) {
            const parsed = JSON.parse(lastMessage.data);
            if (parsed.action === "UPDATE") {
                const updatedJob: Job = parsed.new_record as Job;
                console.log(updatedJob);
                updateJob(updatedJob);
            } 
        }
    },[lastMessage, updateJob])

    useEffect(()=>{
        if (!initialized) {
            // Fetch jobs from the backend and set them in the store
            fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/jobs`,{
                headers: {
                    "ngrok-skip-browser-warning": "true"
                }
            })
                .then(response => response.json())
                .then(data => setJobs(data))
                .catch(error => console.error("Failed to fetch jobs:", error))
        }

    }, [initialized, setJobs])

    return (
        <div className="px-10 flex flex-col gap-6 h-screen">
            <div className="outline outine-1 outine-input rounded-md p-2 w-fit text-muted-foreground">
                <h2 className="font-bold">Debug Info</h2>
                <span>WebSocket Connection: {ReadyState[readyState]}</span>
            </div>

            <div className="p-2 outline-1 outline-input rounded-md">
                <h2 className="font-bold">Tools</h2>
                <NewJobDialog/>
            </div>

            <div className="p-2 outline-1 outline-input rounded-md max-h-1/2 ">
                <h2 className="font-bold">Job Info</h2>
                <JobList className="h-full overflow-scroll scrollbar-custom"/>
            </div>
        </div>
    )
}