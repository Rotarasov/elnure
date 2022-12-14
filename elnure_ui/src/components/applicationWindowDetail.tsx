import { useGet } from "src/api/hooks";
import { Link } from "react-router-dom";
import ApplicationWindow from "../data/applicationWindow";
import Semester from "../data/semester";
import { useEffect, useState } from "react";

const ApplicationWindowDetail = () => {
    const [loading, applicationWindows, errors] = useGet<ApplicationWindow[]>("ref/appwindows", {active: "true"});
    const [currentApplicationWindow, setCurrentApplicationWindow] = useState<ApplicationWindow | null>()
    
    useEffect(() => {
        setCurrentApplicationWindow(applicationWindows ? applicationWindows[0] : null)
        if (currentApplicationWindow && currentApplicationWindow.startDate && currentApplicationWindow.endDate) {
            const startDate = new Date(currentApplicationWindow.startDate)
            const stringStartDate = `${startDate.getHours()}:${startDate.getMinutes()} ${("0" + startDate.getDate()).slice(-2)}.${("0" + (startDate.getMonth() + 1)).slice(-2)}.${startDate.getFullYear()}`

            const endDate = new Date(currentApplicationWindow.endDate)
            const stringEndDate = `${endDate.getHours()}:${endDate.getMinutes()} ${("0" + endDate.getDate()).slice(-2)}.${("0" + (endDate.getMonth() + 1)).slice(-2)}.${endDate.getFullYear()}`

            localStorage.setItem("appwindow", JSON.stringify(currentApplicationWindow))

            setCurrentApplicationWindow({...(currentApplicationWindow ?? {}), startDate: stringStartDate, endDate: stringEndDate})
        }
    }, [applicationWindows])

    return (
        <div className="card">
            <div className="card-header">
                <p>Application window is open! Choose elective subjects wisely</p>
                <p>You must choose elective subject before <b>{currentApplicationWindow?.endDate}</b></p>
            </div>
            <div className="card-body">
                <>
                {currentApplicationWindow?.semesters?.map((semester: Semester, index) => {
                    return (<div className="row my-3 ml-1">{index + 1}.&nbsp;<Link to={`/semester/${semester.id}`}>Choose elective subjects for Semester {semester.id}</Link></div>)
                })}
                </>
            </div>
            <div className="card-footer">
                <Link className="text-center" to={`/application-window/${currentApplicationWindow?.id}/formation-results`}>Go to results page</Link>
            </div>
        </div>
    )
}

export default ApplicationWindowDetail;