import XCTest
import Yams

// MARK: - Config models
struct FlowConfig: Decodable {
    let flows: [Flow]

    struct Flow: Decodable {
        let name: String
        let inputs: [String: String]
        let steps: [Step]
    }

    enum Step: Decodable {
        case fill(selector: String, textFrom: String)
        case tap(selector: String)
        case wait(seconds: Int)
        case screenshot(name: String)

        private enum CodingKeys: String, CodingKey {
            case fill, tap, wait, screenshot
        }

        init(from decoder: Decoder) throws {
            let container = try decoder.container(keyedBy: CodingKeys.self)
            if let map = try? container.decode([String: String].self, forKey: .fill) {
                let selector = map.keys.first!;
                let key = map.values.first!;
                self = .fill(selector: selector, textFrom: key)
            }
            else if let sel = try? container.decode(String.self, forKey: .tap) {
                self = .tap(selector: sel)
            }
            else if let secs = try? container.decode(Int.self, forKey: .wait) {
                self = .wait(seconds: secs)
            }
            else if let name = try? container.decode(String.self, forKey: .screenshot) {
                self = .screenshot(name: name)
            }
            else {
                throw DecodingError.dataCorrupted(.init(
                    codingPath: decoder.codingPath,
                    debugDescription: "Unknown step type"
                ))
            }
        }
    }
}

// MARK: - XCUIElement helper
extension XCUIElement {
    /// Clear existing text then enter new text
    func clearAndEnterText(_ text: String) {
        guard let stringValue = value as? String else {
            self.tap()
            self.typeText(text)
            return
        }
        // Select-all & delete
        let deleteString = String(repeating: XCUIKeyboardKey.delete.rawValue,
                                  count: stringValue.count)
        tap()
        typeText(deleteString)
        typeText(text)
    }
}

// MARK: - YAML-driven UI Tests
class YamlDrivenUITests: XCTestCase {
    var app: XCUIApplication!
    var config: FlowConfig!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()

        // Load and decode YAML
        let bundle = Bundle(for: type(of: self))
        guard let url = bundle.url(forResource: "atdm_flow", withExtension: "yaml") else {
            throw NSError(domain: "YamlDrivenUITests",
                          code: 1,
                          userInfo: [NSLocalizedDescriptionKey: "YAML file not found in bundle"])
        }
        let data = try Data(contentsOf: url)
        config = try YAMLDecoder().decode(FlowConfig.self, from: data)
    }

    func test_login_flow() throws {
        // Find the 'login' flow
        guard let flow = config.flows.first(where: { $0.name == "login" }) else {
            XCTFail("Flow 'login' not defined in YAML")
            return
        }
        run(flow: flow)
    }

    private func run(flow: FlowConfig.Flow) {
        for step in flow.steps {
            switch step {
            case .fill(let selector, let key):
                let text = flow.inputs[key, default: ""]
                let field = app.textFields[selector]
                field.clearAndEnterText(text)

            case .tap(let selector):
                let btn = app.buttons[selector]
                btn.tap()

            case .wait(let seconds):
                sleep(UInt32(seconds))

            case .screenshot(let name):
                let image = XCUIScreen.main.screenshot().pngRepresentation
                let url = URL(fileURLWithPath: NSTemporaryDirectory())
                    .appendingPathComponent("\(name).png")
                try? image.write(to: url)
            }
        }
    }
}
