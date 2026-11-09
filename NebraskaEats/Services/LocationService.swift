import CoreLocation
import Observation
import UIKit

/// "Near me" sorting. Asks for when-in-use permission only when a list is sorted by distance or "My location" is tapped; the location never leaves the device.
@MainActor
@Observable
final class LocationService: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    private(set) var location: CLLocation?
    private(set) var status: CLAuthorizationStatus = .notDetermined
    /// no fix within 12 seconds, or Core Location reported an error
    private(set) var failed = false
    private var timeout: Task<Void, Never>?
    /// when the current request started: a fix from before it is a cached one (from launch, or before a drive) and doesn't count
    private var askedAt = Date.distantPast

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        status = manager.authorizationStatus
    }

    var isDenied: Bool { status == .denied || status == .restricted }

    /// Every place is in Nebraska, so a reader elsewhere (an App Reviewer in California, say) gets told rather than an empty map.
    /// A coarse outline of the state (Idaho's lesson: a bounding box would count Council Bluffs, Sioux City and Yankton),
    /// drawn a little outside the line so the river and bay shores count as inside.
    var isOutsideNebraska: Bool {
        guard let c = location?.coordinate else { return false }
        return !NebraskaOutline.contains(c)
    }

    /// Once location is off for the app, iOS won't ask again; the app's page in Settings is the only way back.
    static func openSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) { UIApplication.shared.open(url) }
    }

    func request() {
        switch manager.authorizationStatus {
        case .notDetermined: manager.requestWhenInUseAuthorization()
        case .authorizedWhenInUse, .authorizedAlways: locate()
        default: break
        }
    }

    private func locate() {
        failed = false
        let asked = Date()
        askedAt = asked
        manager.requestLocation()
        timeout?.cancel()
        timeout = Task { [weak self] in
            try? await Task.sleep(for: .seconds(12))
            guard let self, !Task.isCancelled else { return }
            if (self.location?.timestamp ?? .distantPast) < asked { self.failed = true }
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ m: CLLocationManager) {
        let s = m.authorizationStatus
        Task { @MainActor in
            self.status = s
            if s == .authorizedWhenInUse || s == .authorizedAlways { self.locate() }
        }
    }

    nonisolated func locationManager(_ m: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let l = locations.last else { return }
        Task { @MainActor in
            // "My location" needs a fresh fix on every tap: a cached one from before the request would put you back where you were
            guard l.timestamp >= self.askedAt.addingTimeInterval(-2) else { return }
            self.location = l; self.failed = false; self.timeout?.cancel()
        }
    }

    nonisolated func locationManager(_ m: CLLocationManager, didFailWithError error: Error) {
        Task { @MainActor in if self.location == nil { self.failed = true } }
    }
}

extension CLLocation {
    /// "0.4 mi", "12 mi", "1,012 mi" (an App Reviewer in California is a thousand miles out)
    func milesText(to other: CLLocation) -> String {
        let mi = distance(from: other) / 1609.344
        return (mi < 10 ? mi.formatted(.number.precision(.fractionLength(1))) : Int(mi.rounded()).formatted()) + " mi"
    }
}

/// A coarse Nebraska outline (longitude, latitude), about 600 m outside the Overture land outline but never over a neighbour's land
/// (buffer 0.006°, the neighbours cut back out, simplify 0.008°). Omaha, Lincoln, South Sioux City, Scottsbluff, Harrison, Falls City,
/// Plattsmouth, Nebraska City and Valentine are inside; Council Bluffs, Sioux City, Yankton, North Sioux City, Elk Point, Pine Bluffs,
/// Julesburg, Hiawatha, Rock Port and Hamburg are not.
enum NebraskaOutline {
    static let rings: [[(Double, Double)]] = [
        [(-95.3081, 40.0), (-102.0518, 40.0032), (-102.0516, 41.0024), (-104.0532, 41.0017), (-104.0532, 43.0013), (-98.4985, 42.9986), (-98.4441, 42.9292), (-98.4207, 42.9319), (-98.1898, 42.8416), (-98.1469, 42.8398), (-98.035, 42.7642), (-97.9368, 42.7793), (-97.8884, 42.822), (-97.8754, 42.8587), (-97.8455, 42.8678), (-97.7771, 42.8366), (-97.7213, 42.8624), (-97.6759, 42.8313), (-97.6268, 42.8642), (-97.6267, 42.8466), (-97.5195, 42.86), (-97.4449, 42.8459), (-97.4145, 42.867), (-97.3526, 42.8742), (-97.2207, 42.8468), (-97.2101, 42.8093), (-97.1508, 42.7956), (-97.1303, 42.7715), (-97.0656, 42.7722), (-96.9604, 42.7482), (-96.9474, 42.7171), (-96.9079, 42.7327), (-96.8656, 42.7294), (-96.8348, 42.7041), (-96.8064, 42.702), (-96.7931, 42.6663), (-96.6966, 42.6524), (-96.711, 42.6071), (-96.6841, 42.5766), (-96.6386, 42.5527), (-96.6174, 42.5078), (-96.5447, 42.5187), (-96.499, 42.482), (-96.4368, 42.4901), (-96.3858, 42.475), (-96.3805, 42.4451), (-96.415, 42.4057), (-96.4084, 42.3761), (-96.4178, 42.3514), (-96.3753, 42.3183), (-96.3658, 42.2859), (-96.3289, 42.2547), (-96.3237, 42.2299), (-96.3599, 42.2105), (-96.3478, 42.1668), (-96.2689, 42.1136), (-96.2755, 42.052), (-96.2219, 42.0296), (-96.2407, 41.9994), (-96.1946, 42.0087), (-96.1836, 42.0), (-96.1856, 41.9778), (-96.1295, 41.9717), (-96.1446, 41.9415), (-96.1367, 41.9208), (-96.1618, 41.9018), (-96.142, 41.8689), (-96.1102, 41.8488), (-96.1076, 41.8207), (-96.0649, 41.7962), (-96.0799, 41.7579), (-96.1064, 41.7379), (-96.0731, 41.705), (-96.1214, 41.6885), (-96.095, 41.6474), (-96.1176, 41.61), (-96.0812, 41.5773), (-96.0941, 41.5393), (-96.0407, 41.5071), (-96.0273, 41.5411), (-96.0012, 41.5411), (-95.9928, 41.512), (-96.0192, 41.4893), (-96.0118, 41.4762), (-95.9368, 41.4652), (-95.9203, 41.4516), (-95.9369, 41.3964), (-95.9288, 41.3701), (-95.956, 41.3431), (-95.9258, 41.3216), (-95.8856, 41.3181), (-95.8719, 41.3018), (-95.8761, 41.2857), (-95.9028, 41.2744), (-95.9132, 41.2795), (-95.9045, 41.2995), (-95.928, 41.2985), (-95.9106, 41.2346), (-95.9278, 41.1997), (-95.9161, 41.1853), (-95.8638, 41.1882), (-95.8422, 41.1774), (-95.8462, 41.1667), (-95.8813, 41.1599), (-95.8626, 41.0884), (-95.8824, 41.0604), (-95.8597, 41.0357), (-95.8673, 41.0016), (-95.8299, 40.9778), (-95.8397, 40.9328), (-95.8095, 40.8912), (-95.8478, 40.8643), (-95.8342, 40.783), (-95.8836, 40.7478), (-95.8853, 40.7211), (-95.8526, 40.7023), (-95.8428, 40.6775), (-95.7866, 40.6573), (-95.7497, 40.6068), (-95.7739, 40.5759), (-95.7652, 40.5298), (-95.7087, 40.5213), (-95.6951, 40.5331), (-95.694, 40.5569), (-95.6786, 40.5625), (-95.6557, 40.5466), (-95.6617, 40.5173), (-95.7004, 40.5051), (-95.6943, 40.4718), (-95.6571, 40.4398), (-95.6605, 40.4124), (-95.6237, 40.3466), (-95.6566, 40.3109), (-95.6107, 40.3137), (-95.5638, 40.298), (-95.5519, 40.2888), (-95.5505, 40.2603), (-95.4774, 40.2426), (-95.4697, 40.2252), (-95.4792, 40.1862), (-95.4363, 40.1587), (-95.4267, 40.1338), (-95.3933, 40.1187), (-95.4207, 40.061), (-95.4153, 40.0405), (-95.3896, 40.0266), (-95.35, 40.0299), (-95.3081, 40.0)]
    ]

    static func contains(_ c: CLLocationCoordinate2D) -> Bool { rings.contains { contains(c, ring: $0) } }

    /// Ray casting: a point is inside when a ray east of it crosses the outline an odd number of times.
    static func contains(_ c: CLLocationCoordinate2D, ring: [(Double, Double)]) -> Bool {
        var inside = false
        var j = ring.count - 1
        for i in 0..<ring.count {
            let (xi, yi) = ring[i], (xj, yj) = ring[j]
            if (yi > c.latitude) != (yj > c.latitude) && c.longitude < (xj - xi) * (c.latitude - yi) / (yj - yi) + xi { inside.toggle() }
            j = i
        }
        return inside
    }
}
