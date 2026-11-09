import SwiftUI
import UIKit
import CoreText

/// Nebraska palette (Nick's decision, 2026-11-07; playbook/05-naming.md), light only, from the land rather than the team: prairie-sky blue
/// #1D4E7A (8.7:1 on white, 7.7:1 on cream) for titles, tint, the honors and oldest cards; charcoal #1F1F1F (white on it 16.6:1) for the
/// hand-checked guide cards and ink; Sandhills-grass gold #C9A24B only as a pin, title-shadow and header fill under ink (as text on white
/// it fails, 2.4:1); cream #F5F1E7 pages. The names `green`/`gold` are kept from Wisconsin Eats so the shared views read the same; here
/// `green` is prairie-sky blue and `gold` is charcoal.
enum Theme {
    static let green = Color(hex: 0x1D4E7A)      // prairie-sky blue: titles, tint, primary text accents
    static let green2 = Color(hex: 0x245A8A)     // a lighter sky blue for small labels (7.2:1 on white)
    static let gold = Color(hex: 0x1F1F1F)       // charcoal: card fills under white text, chips
    static let goldSoft = Color(hex: 0xECE6DA)   // soft warm gray
    static let lime = Color(hex: 0xC9A24B)       // Sandhills-grass gold, fills only (hand-checked pins, the title shadow), under ink
    static let limeSoft = Color(hex: 0xF1E6C8)
    static let sand = Color(hex: 0xF5F1E7)       // the Home background, cream
    static let red = Color(hex: 0x1D4E7A)        // honors chips (prairie-sky blue)
    static let sandstone = Color(hex: 0x143A5C)  // a darker sky blue accent
    static let teal = Color(hex: 0x1D4E7A)       // prairie-sky blue (8.7:1 on white)
    static let ink = Color(hex: 0x1F1F1F)
    static let ink2 = Color(hex: 0x2E3440)
    static let muted = Color(hex: 0x5B6270)
    static let surface = Color.white
    static let surface2 = Color(hex: 0xEFE9DC)
    static let surface3 = Color(hex: 0xE4DCC8)
    static let rule = Color(hex: 0xE4DCC8)
    static let rule2 = Color(hex: 0xCBC1A8)
}

extension Color {
    init(hex: UInt32) {
        self.init(red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255, blue: Double(hex & 0xFF) / 255)
    }
}

/// A small uppercase label: "STONE CRAB", "1 MICHELIN STAR".
struct Chip: View {
    enum Style { case gold, green, red, plain, dashed }
    let text: String
    var style: Style = .plain

    var body: some View {
        Text(text.uppercased())
            .font(.caption2.weight(.bold))
            .tracking(0.4)
            .padding(.horizontal, 7).padding(.vertical, 3)
            .foregroundStyle(style == .green || style == .red ? Color.white : style == .dashed ? Theme.muted : style == .gold ? Theme.ink : Theme.green)
            .background {
                RoundedRectangle(cornerRadius: 5).fill(style == .gold ? Theme.goldSoft : style == .green ? Theme.green : style == .red ? Theme.red
                                                       : style == .dashed ? .clear : Theme.surface2)
            }
            .overlay {
                if style == .dashed { RoundedRectangle(cornerRadius: 5).strokeBorder(Theme.rule2, style: StrokeStyle(lineWidth: 1, dash: [3, 2])) }
            }
            .accessibilityLabel(text)
    }
}

/// Nebraska Eats' lettering: the system face drawn compressed and heavy for titles and guide names (like a show poster), and the
/// system monospaced face for numbers, dates and small labels. No bundled fonts.
struct DisplayFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .black
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight).width(.compressed))
    }
}

/// Numbers, dates and small labels in the system monospaced face, scaled like DisplayFont.
struct MonoFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .semibold
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight, design: .monospaced))
    }
}

extension View {
    func displayFont(_ size: CGFloat, weight: Font.Weight = .black) -> some View {
        modifier(DisplayFont(size: size, weight: weight))
    }

    func monoFont(_ size: CGFloat, weight: Font.Weight = .semibold) -> some View {
        modifier(MonoFont(size: size, weight: weight))
    }
}

/// The header band: a prairie horizon with Chimney Rock's spire on it, the Oregon Trail landmark in the Panhandle: wheat-gold ground
/// under a charcoal horizon line, the rock a charcoal silhouette.
struct Stripes: View {
    var height: CGFloat = 6

    var body: some View {
        Canvas { ctx, size in
            let w = size.width, h = size.height, ground = h * 0.64
            ctx.fill(Path(CGRect(x: 0, y: ground, width: w, height: h - ground)), with: .color(Theme.lime))
            ctx.fill(Path(CGRect(x: 0, y: ground - 1, width: w, height: 1.5)), with: .color(Theme.ink))
            // Chimney Rock: a broad cone of clay and ash, a narrow spire on top
            let cx = w * 0.8
            var rock = Path()
            rock.move(to: CGPoint(x: cx - h * 1.3, y: ground))
            rock.addQuadCurve(to: CGPoint(x: cx - h * 0.16, y: h * 0.34), control: CGPoint(x: cx - h * 0.45, y: ground - h * 0.04))
            rock.addLine(to: CGPoint(x: cx - h * 0.09, y: 0))
            rock.addLine(to: CGPoint(x: cx + h * 0.09, y: 0))
            rock.addLine(to: CGPoint(x: cx + h * 0.16, y: h * 0.34))
            rock.addQuadCurve(to: CGPoint(x: cx + h * 1.3, y: ground), control: CGPoint(x: cx + h * 0.45, y: ground - h * 0.04))
            rock.closeSubpath()
            ctx.fill(rock, with: .color(Theme.ink))
        }
        .frame(height: height * 2.4)
        .accessibilityHidden(true)
    }
}

extension View {
    /// An inline navigation title in the display type. UINavigationBar.appearance() didn't reach every SwiftUI bar on iOS 27
    /// (the Map title went from compressed blue to plain black after a push and pop; place titles were always plain), so the
    /// title is our own view in the bar. The navigation title is still set, for the back button and VoiceOver.
    func inlineTitle(_ title: String) -> some View {
        navigationTitle(title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text(title).displayFont(19, weight: .heavy).foregroundStyle(Theme.green)
                        .lineLimit(1).minimumScaleFactor(0.7)
                        .accessibilityAddTraits(.isHeader)
                }
            }
    }
}
