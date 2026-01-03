import Foundation
import EventKit

let args = CommandLine.arguments
guard args.count == 6 else {
    print("Usage: SetReminder <title> <date> <start_time> <end_time> <description>")
    exit(1)
}

let title = args[1]
let date = args[2]         // "YYYY-MM-DD"
let startTime = args[3]    // "HH:MM"
let endTime = args[4]      // "HH:MM"
let description = args[5]

let eventStore = EKEventStore()
let status = EKEventStore.authorizationStatus(for: .event)
if status == .authorized {
    // Already authorized, create event synchronously
    let event = EKEvent(eventStore: eventStore)
    event.title = title
    event.notes = description

    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd HH:mm"
    guard let startDate = formatter.date(from: "\(date) \(startTime)"),
          let endDate = formatter.date(from: "\(date) \(endTime)") else {
        print("Invalid date/time format")
        exit(1)
    }
    event.startDate = startDate
    event.endDate = endDate
    event.calendar = eventStore.defaultCalendarForNewEvents

    do {
        try eventStore.save(event, span: .thisEvent)
        print("Event created successfully")
        exit(0)
    } catch {
        print("Failed to save event: \(error)")
        exit(1)
    }
} else if status == .notDetermined {
    eventStore.requestAccess(to: .event) { (granted, error) in
    guard granted else {
        print("Access to calendar not granted")
        exit(1)
    }
    let event = EKEvent(eventStore: eventStore)
    event.title = title
    event.notes = description

    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd HH:mm"
    guard let startDate = formatter.date(from: "\(date) \(startTime)"),
          let endDate = formatter.date(from: "\(date) \(endTime)") else {
        print("Invalid date/time format")
        exit(1)
    }
    event.startDate = startDate
    event.endDate = endDate
    event.calendar = eventStore.defaultCalendarForNewEvents

    do {
        try eventStore.save(event, span: .thisEvent)
        print("Event created successfully")
        exit(0)
    } catch {
        print("Failed to save event: \(error)")
        exit(1)
    }
    }
    RunLoop.main.run()
} else {
    print("Access to calendar not granted")
    exit(1)
}