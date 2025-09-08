import { createResource } from "frappe-ui"
import { employeeResource } from "./employee"
import dayjs from "@/utils/dayjs"

// Function to format WFH request dates
export const getDates = (wfh) => {
    if (!wfh.from_date || !wfh.to_date) return "Invalid Date";
    if (wfh.from_date === wfh.to_date)
        return dayjs(wfh.from_date).format("D MMM");
    return `${dayjs(wfh.from_date).format("D MMM")} - ${dayjs(wfh.to_date).format("D MMM")}`;
};

// Function to transform WFH data
const transformWorkFromHomeData = (data) => {
    return data.map((wfh) => {
        if (process.env.NODE_ENV !== 'production') {
            console.log("Processing WFH Request:", wfh.name, "From Date:", wfh.from_date, "To Date:", wfh.to_date);
        }
        wfh.wfh_dates = getDates(wfh);
        wfh.doctype = "Work From Home";
        return wfh;
    });
};

// My WFH Requests
export const myWFH = createResource({
    url: "hrms.api.get_work_from_home",
    params: {
        employee: employeeResource.data?.name || "",
        limit: 10,
    },
    auto: true,
    cache: "hrms:my_wfh",
    transform(data) {
        return transformWorkFromHomeData(data);
    },
});

// Team WFH Requests (For Approver)
export const teamWFH = createResource({
    url: "hrms.api.get_work_from_home",
    params: {
        employee: employeeResource.data?.name || "",
        approver_id: employeeResource.data?.user_id || "",
        for_approval: 1,
        limit: 10,
    },
    auto: true,
    cache: "hrms:team_wfh",
    transform(data) {
        return transformWorkFromHomeData(data);
    },
});





