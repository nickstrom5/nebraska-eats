import Foundation
import CoreLocation
import UIKit

/// `-screenshot <name>` opens one screen with fixed state for App Store screenshots (scripts/capture-screenshots.sh).
/// Names: home, steaks, reubens, taquerias, honors, oldest, detail, map, saved, about.
enum ScreenshotMode {
    /// Debug builds only: an App Store build ignores the launch argument, so no one can reach seeded screens or fake locations.
    static var name: String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: "-screenshot"), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
    static var isActive: Bool { name != nil }

    @MainActor
    static func apply(to model: AppModel) {
        guard let name, model.isLoaded else { return }
        model.filters = Filters()
        // downtown Omaha (the Old Market), so "nearest" lists have distances without a permission prompt
        model.screenshotLocation = CLLocation(latitude: 41.2556, longitude: -95.9310)
        // by name and town, ignoring case, so a rebuild with a slightly different casing still finds the place; the hand-checked one first
        let pick = { (n: String, town: String?) -> Place? in
            let hits = model.places.filter { $0.name.caseInsensitiveCompare(n) == .orderedSame && (town == nil || $0.city == town) }
            return hits.first(where: \.handChecked) ?? hits.first
        }
        for p in [pick("Johnny's Cafe", "Omaha"), pick("Crescent Moon Ale House", "Omaha"), pick("Glur's Tavern", "Columbus")]
            .compactMap({ $0 }) where !model.isSaved(p) {
            model.toggleSaved(p)
        }
        let open = { (g: Guide) in model.tab = .guides; model.selectedGuide = g; model.guidesPath = [.guide(g)] }
        switch name {
        case "steaks":
            // central Omaha (Aksarben), among the city's steakhouses
            model.screenshotLocation = CLLocation(latitude: 41.2420, longitude: -96.0100)
            open(.steaks)
        case "reubens":
            // Blackstone, where Omaha says the Reuben was first made
            model.screenshotLocation = CLLocation(latitude: 41.2588, longitude: -95.9700)
            open(.reubens)
        case "taquerias":
            // South 24th Street, South Omaha
            model.screenshotLocation = CLLocation(latitude: 41.2112, longitude: -95.9470)
            open(.taquerias)
        case "honors": open(.honors)
        case "oldest": open(.oldest)
        case "detail":
            // Johnny's Cafe: the 1922 Stockyards steakhouse, with its note and its America's Classic
            model.screenshotLocation = CLLocation(latitude: 41.2420, longitude: -96.0100)
            open(.steaks)
            if let p = pick("Johnny's Cafe", "Omaha") ?? model.places.first {
                model.selectedPlace = p; model.guidesPath.append(.place(p))
            }
        case "map": model.tab = .map
        case "saved": model.tab = .saved
        case "about": model.tab = .about
        default: model.tab = .guides; model.selectedGuide = nil
        }
        // iPad shows the place column next to every list, so give each shot a place instead of "Pick a place": a different
        // honored or hand-checked one per shot.
        guard UIDevice.current.userInterfaceIdiom == .pad, model.selectedPlace == nil else { return }
        let place: Place? = switch name {
        case "home": pick("Glur's Tavern", "Columbus")
        case "steaks": pick("The Drover", "Omaha")
        case "reubens": pick("Crescent Moon Ale House", "Omaha")
        case "taquerias": pick("Taquería El Rey", "Omaha")
        case "map": pick("Gorat's", "Omaha")
        case "honors": pick("Johnny's Cafe", "Omaha")
        case "oldest": pick("Glur's Tavern", "Columbus")
        case "saved": pick("Johnny's Cafe", "Omaha")
        case "about": nil
        default: pick("Johnny's Cafe", "Omaha")
        }
        model.selectedPlace = place
    }
}
