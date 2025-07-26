import JobForm from "@/components/jobs/job-form"
import JobList from "@/components/jobs/job-list"
import { useJobStore } from "@/stores/useJobsStore"
import { useEffect } from "react"
export default function ManageJobsPage() {
    const { setJobs, initialized } = useJobStore()
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
        <div>
            <JobList/>
            <JobForm />
        </div>
    )
}