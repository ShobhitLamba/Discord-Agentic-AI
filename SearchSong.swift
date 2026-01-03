import Foundation

// Usage: SearchSong <song> [artist]

let args = CommandLine.arguments

guard args.count >= 2 else {
    print("Usage: SearchSong <song> [artist]")
    exit(1)
}

let song = args[1]
let artist = args.count > 2 ? args[2] : nil

// Build search query for Apple Music
var searchQuery = song
if let artist = artist {
    searchQuery += " \(artist)"
}

// Encode the search query for URL
guard let encodedQuery = searchQuery.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) else {
    print("Failed to encode search query")
    exit(1)
}

// Use Apple Music URL scheme to open and search
let appleMusicURL = "music://music.apple.com/us/search?term=\(encodedQuery)"

let task = Process()
task.launchPath = "/usr/bin/open"
task.arguments = [appleMusicURL]

do {
    try task.run()
    task.waitUntilExit()
    print("Opened Apple Music with search: \(searchQuery)")
    exit(0)
} catch {
    print("Failed to open Apple Music: \(error)")
    exit(1)
}

