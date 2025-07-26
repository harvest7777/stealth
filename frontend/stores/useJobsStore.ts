import { create } from "zustand";

interface JobState {
    jobs: Job[] | null;
    initialized: boolean;
}

interface JobActions {
    setJobs: (jobs: Job[]) => void;
    addJob: (job: Job) => void;
    removeJob: (id: string) => void;
    updateJob: (job: Job) => void;
}

export const useJobStore = create<JobState & JobActions>((set) => ({
    // State
    jobs: null,
    initialized: false,

    // Actions
    setJobs: (jobs) =>
    set(() => ({
      jobs,
      initialized: true,
    })),

    addJob: (job) =>
    set((state) => ({
      jobs: state.jobs ? [...state.jobs, job] : [job],
    })),

    removeJob: (id) =>
    set((state) => ({
      jobs: state.jobs ? state.jobs.filter((job) => job.id !== id) : null,
    })),
    updateJob: (newJob) =>
    set((state) => ({
      jobs: state.jobs
        ? state.jobs.map((job) => (job.id === newJob.id ? newJob : job))
        : null,
    })),
}));
