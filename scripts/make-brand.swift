// Nebraska Eats brand (Nick's decision, 2026-11-07: the name, icon C and the prairie-sky palette): the app icon is concept C of
// scripts/icon-concepts.swift, a Reuben in side elevation (rye, corned beef, Swiss, sauerkraut, rye), on prairie-sky blue; the shared Eats Ranked
// icon style, state-prompts/ICON-STYLE.md, no backing shape. No N, Herbie Husker, team words or university marks; no state seal.
// Usage, from ne-eats/: swift scripts/make-brand.swift   -> NebraskaEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png,
// docs/ favicons and touch icons, docs/og.png. scripts/make-site.py draws the same mark as its inline SVG (LOGO): change both together.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let SKY: UInt32 = 0x1D4E7A, RYE: UInt32 = 0x8B5A2B, BEEF: UInt32 = 0xB5473A, SWISS: UInt32 = 0xF2E2A0, KRAUT: UInt32 = 0xE5DDB0
let CREAM: UInt32 = 0xF5F1E7, WHEAT: UInt32 = 0xC9A24B, INK: UInt32 = 0x1F1F1F

func R(_ s: CGFloat, _ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat, _ r: CGFloat) -> CGPath {
    CGPath(roundedRect: CGRect(x: x * s, y: y * s, width: w * s, height: h * s), cornerWidth: r * s, cornerHeight: r * s, transform: nil)
}

/// C: the Reuben. CoreGraphics y-up, s = canvas size. Identical to icon-concepts.swift's concept C.
func reuben(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(RYE)); c.addPath(R(s, 0.14, 0.24, 0.72, 0.11, 0.045)); c.fillPath()     // the bottom slice of rye
    c.setFillColor(rgb(BEEF)); c.addPath(R(s, 0.16, 0.34, 0.68, 0.13, 0.05)); c.fillPath()     // the corned beef
    c.setFillColor(rgb(SWISS)); c.addPath(R(s, 0.15, 0.46, 0.70, 0.05, 0.02)); c.fillPath()    // the Swiss, melted past the edge
    c.setFillColor(rgb(KRAUT)); c.addPath(R(s, 0.17, 0.50, 0.66, 0.07, 0.03)); c.fillPath()    // the sauerkraut
    c.setFillColor(rgb(RYE)); c.addPath(R(s, 0.14, 0.56, 0.72, 0.13, 0.05)); c.fillPath()      // the top slice
}

func render(_ n: Int, _ path: String, background: Bool) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: background ? CGImageAlphaInfo.noneSkipLast.rawValue : CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.setShouldAntialias(true)
    if background { ctx.setFillColor(rgb(SKY)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n)) }
    reuben(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
render(1024, "NebraskaEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png", background: true)
try? FileManager.default.createDirectory(atPath: "docs", withIntermediateDirectories: true)
for (n, name) in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")] {
    render(n, "docs/" + name, background: true)
}

/// The share image (1200 x 630): prairie-sky blue, the Reuben at the left, the name and tagline at the right, and the app's header band along
/// the bottom: a prairie horizon with Chimney Rock's spire, wheat-gold ground under a charcoal line (Theme.swift's Stripes).
func og(_ path: String) {
    let W = 1200, H = 630
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(SKY)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    let band: CGFloat = 70, ground: CGFloat = 26
    ctx.setFillColor(rgb(CREAM)); ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(W), height: band))
    ctx.setFillColor(rgb(WHEAT)); ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(W), height: ground))
    ctx.setFillColor(rgb(INK)); ctx.fill(CGRect(x: 0, y: ground, width: CGFloat(W), height: 3))
    let cx: CGFloat = 960
    let rock = CGMutablePath()
    rock.move(to: CGPoint(x: cx - 70, y: ground))
    rock.addQuadCurve(to: CGPoint(x: cx - 9, y: ground + 26), control: CGPoint(x: cx - 24, y: ground + 4))
    rock.addLine(to: CGPoint(x: cx - 5, y: band - 4)); rock.addLine(to: CGPoint(x: cx + 5, y: band - 4))
    rock.addLine(to: CGPoint(x: cx + 9, y: ground + 26))
    rock.addQuadCurve(to: CGPoint(x: cx + 70, y: ground), control: CGPoint(x: cx + 24, y: ground + 4))
    rock.closeSubpath()
    ctx.addPath(rock); ctx.fillPath()
    ctx.saveGState(); ctx.translateBy(x: 40, y: 90); reuben(ctx, 500); ctx.restoreGState()
    let ns = NSGraphicsContext(cgContext: ctx, flipped: false)
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ns
    let title = NSFont(name: "AvenirNextCondensed-Heavy", size: 80) ?? NSFont.boldSystemFont(ofSize: 70)
    let sub = NSFont(name: "AvenirNextCondensed-DemiBold", size: 34) ?? NSFont.boldSystemFont(ofSize: 30)
    NSAttributedString(string: "NEBRASKA", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 560, y: 380))
    NSAttributedString(string: "EATS", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 560, y: 296))
    NSAttributedString(string: "STEAKS, REUBENS & TAQUERÍAS", attributes: [.font: sub, .foregroundColor: NSColor(srgbRed: 0.961, green: 0.945, blue: 0.906, alpha: 1)]).draw(at: NSPoint(x: 564, y: 246))
    NSGraphicsContext.restoreGraphicsState()
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
og("docs/og.png")
