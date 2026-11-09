// Nebraska Eats icon concepts (2026-11-06), drawn in the shared Eats Ranked style (state-prompts/ICON-STYLE.md): one flat, level, centred
// food on prairie-sky blue #1D4E7A (Nick's decision, 2026-11-07; no N, mascot or team marks), no backing shape, no text or texture.
// Food hexes: fat #F3E2C0, seared beef #6E3B1F, bone #FBF6EC; bread crust #C98A3D, crumb #F2D29A, cabbage #C9D98F; rye #8B5A2B,
// corned beef #B5473A, Swiss #F2E2A0, sauerkraut #E5DDB0.
//   A  a T-bone steak, top view: the fat rim, the seared meat and the T of the bone
//   B  a bierock cut open: the bun, its crumb, and the beef-and-cabbage filling
//   C  a Reuben, side elevation: rye, corned beef, Swiss, sauerkraut, rye
// Skipped, per the prompt: corn (the Iowa build's idea, and it leans Husker).
// Usage, from ne-eats/: swift scripts/icon-concepts.swift <out dir>   -> concept-{a,b,c}-1024.png
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let SKY: UInt32 = 0x1D4E7A, FAT: UInt32 = 0xF3E2C0, MEAT: UInt32 = 0x6E3B1F, BONE: UInt32 = 0xFBF6EC
let CRUST: UInt32 = 0xC98A3D, CRUMB: UInt32 = 0xF2D29A, CABBAGE: UInt32 = 0xC9D98F
let RYE: UInt32 = 0x8B5A2B, BEEF: UInt32 = 0xB5473A, SWISS: UInt32 = 0xF2E2A0, KRAUT: UInt32 = 0xE5DDB0

func R(_ s: CGFloat, _ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat, _ r: CGFloat) -> CGPath {
    CGPath(roundedRect: CGRect(x: x * s, y: y * s, width: w * s, height: h * s), cornerWidth: r * s, cornerHeight: r * s, transform: nil)
}

/// A: the T-bone. CoreGraphics y-up. Identical to make-brand.swift's tbone() and make-site.py's LOGO.
func tbone(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(FAT)); c.addPath(R(s, 0.14, 0.24, 0.72, 0.52, 0.20)); c.fillPath()          // the fat rim
    c.setFillColor(rgb(MEAT)); c.addPath(R(s, 0.175, 0.275, 0.65, 0.45, 0.166)); c.fillPath()      // the seared meat
    c.setFillColor(rgb(BONE))
    c.addPath(R(s, 0.22, 0.62, 0.56, 0.06, 0.03)); c.fillPath()                                    // the bone's crossbar, along the top
    c.addPath(R(s, 0.55, 0.30, 0.06, 0.38, 0.03)); c.fillPath()                                    // and its stem, strip on one side, tenderloin on the other
}

/// B: a bierock cut open: the bun's crust, its crumb, and the beef-and-cabbage filling.
func bierock(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(CRUST)); c.addPath(R(s, 0.16, 0.26, 0.68, 0.48, 0.24)); c.fillPath()
    c.setFillColor(rgb(CRUMB)); c.addPath(R(s, 0.20, 0.30, 0.60, 0.40, 0.20)); c.fillPath()
    c.setFillColor(rgb(MEAT)); c.addPath(R(s, 0.28, 0.37, 0.44, 0.26, 0.12)); c.fillPath()
    c.setFillColor(rgb(CABBAGE))
    for (x, y) in [(0.34, 0.47), (0.47, 0.41), (0.58, 0.50)] as [(CGFloat, CGFloat)] { c.addPath(R(s, x, y, 0.09, 0.05, 0.025)); c.fillPath() }
}

/// C: a Reuben, side elevation.
func reuben(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(RYE)); c.addPath(R(s, 0.14, 0.24, 0.72, 0.11, 0.045)); c.fillPath()
    c.setFillColor(rgb(BEEF)); c.addPath(R(s, 0.16, 0.34, 0.68, 0.13, 0.05)); c.fillPath()
    c.setFillColor(rgb(SWISS)); c.addPath(R(s, 0.15, 0.46, 0.70, 0.05, 0.02)); c.fillPath()
    c.setFillColor(rgb(KRAUT)); c.addPath(R(s, 0.17, 0.50, 0.66, 0.07, 0.03)); c.fillPath()
    c.setFillColor(rgb(RYE)); c.addPath(R(s, 0.14, 0.56, 0.72, 0.13, 0.05)); c.fillPath()
}

func render(_ n: Int, _ path: String, _ draw: (CGContext, CGFloat) -> Void) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(SKY)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n))
    draw(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "playbook/brand"
render(1024, out + "/concept-a-1024.png", tbone)
render(1024, out + "/concept-b-1024.png", bierock)
render(1024, out + "/concept-c-1024.png", reuben)
