import 'dart:math'; // For random number generation
import 'package:flutter/material.dart'; // Flutter UI toolkit
import 'package:flutter/services.dart' show rootBundle, SystemChrome, SystemUiMode, SystemNavigator; // For loading assets, SystemChrome, and SystemNavigator
import 'package:url_launcher/url_launcher.dart'; // Add this import at the top with the others

void main() {
  WidgetsFlutterBinding.ensureInitialized(); // Ensure binding for SystemChrome
  // Set the app to immersive mode (hides system UI, user can swipe to reveal)
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  runApp(const CreatureTypeGeneratorApp());
}

// The root widget of the application
class CreatureTypeGeneratorApp extends StatelessWidget {
  const CreatureTypeGeneratorApp({super.key});

  @override
  Widget build(BuildContext context) {
    // MaterialApp sets up app-wide configuration, theme, and navigation
    return MaterialApp(
      title: 'MTG Creature Type Generator',
      // Set up a dark theme with custom colors
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF23272A), // dark grey background
        colorScheme: ThemeData.dark().colorScheme.copyWith(
          primary: Colors.blue[300], // lighter blue for buttons, etc.
          secondary: Colors.blue[200], // lighter blue for secondary elements
        ),
        textTheme: ThemeData.dark().textTheme.apply(
              bodyColor: Colors.blue[200], // lighter blue for body text
              displayColor: Colors.blue[200], // lighter blue for display text
            ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF2C2F33), // slightly lighter dark grey for app bar
          foregroundColor: Color(0xFF90CAF9), // lighter blue for app bar text
          centerTitle: true, // center the title in the app bar
        ),
      ),
      home: const CreatureTypeGeneratorScreen(), // Main screen of the app
      debugShowCheckedModeBanner: false, // Hide the debug banner
    );
  }
}

// The main screen widget, stateful because it manages dynamic data
class CreatureTypeGeneratorScreen extends StatefulWidget {
  const CreatureTypeGeneratorScreen({super.key});

  @override
  State<CreatureTypeGeneratorScreen> createState() => _CreatureTypeGeneratorScreenState();
}

// State class for the main screen
class _CreatureTypeGeneratorScreenState extends State<CreatureTypeGeneratorScreen> {
  List<String> _creatureTypes = []; // List of all possible creature types loaded from file
  final List<String> _history = []; // List of generated creature types (history)
  bool _isLoading = true; // Whether the app is still loading the creature types

  // Maximum number of history entries allowed to prevent excessive memory use
  static const int _maxHistoryLength = 100;

  @override
  void initState() {
    super.initState();
    _loadCreatureTypes(); // Load creature types from the asset file when the widget is created
  }

  // Loads the creature types from the assets/creature_types.txt file
  Future<void> _loadCreatureTypes() async {
    final String data = await rootBundle.loadString('assets/creature_types.txt');
    setState(() {
      // Split the file into lines, trim whitespace, and remove empty lines
      _creatureTypes = data.split('\n').map((e) => e.trim()).where((e) => e.isNotEmpty).toList();
      _isLoading = false; // Loading is complete
    });
  }

  // Generates a random creature type and adds it to the history
  void _generateCreatureType() {
    if (_creatureTypes.isEmpty) return; // Do nothing if the list is empty

    // Prevent adding more than the maximum allowed history entries
    if (_history.length >= _maxHistoryLength) return;

    final random = Random();
    final creature = _creatureTypes[random.nextInt(_creatureTypes.length)];
    setState(() {
      _history.insert(0, creature); // Insert the new creature at the start of the history
    });
  }

  // Clears the history (starts a new game)
  void _newGame() {
    setState(() {
      _history.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    // Scaffold provides the basic visual layout structure
    return Scaffold(
      // Add a Drawer for slide-out navigation
      drawer: Drawer(
        // The Drawer widget provides a slide-out navigation panel from the left
        child: Container(
          color: const Color(0xFF23272A), // Match the app's dark background
          child: Column(
            children: [
              // The scrollable list of navigation items
              Expanded(
                child: ListView(
                  padding: EdgeInsets.zero,
                  children: [
                    // Drawer header with app title
                    DrawerHeader(
                      decoration: const BoxDecoration(
                        color: Color(0xFF2C2F33), // Slightly lighter for header
                      ),
                      child: Center(
                        child: Text(
                          'MTG\nCreature Type Generator',
                          style: TextStyle(
                            color: Colors.blue[200],
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    // Example navigation items (add more as needed)
                    ListTile(
                      leading: const Icon(Icons.home, color: Color(0xFF90CAF9)),
                      title: const Text('Home', style: TextStyle(color: Color(0xFF90CAF9))),
                      onTap: () {
                        Navigator.pop(context); // Close the drawer
                        // Add navigation logic here if needed
                      },
                    ),
                    ListTile(
                      leading: const Icon(Icons.list, color: Color(0xFF90CAF9)),
                      title: const Text('Deck List', style: TextStyle(color: Color(0xFF90CAF9))),
                      onTap: () async {
                        Navigator.pop(context); // Close the drawer
                        // URL to open (replace with your actual deck list URL)
                        const url = 'https://archidekt.com/decks/11260057/tribal_squared';
                        // Check if the URL can be launched, then launch it
                        if (await canLaunchUrl(Uri.parse(url))) {
                          await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
                        }
                      },
                    ),
                  ],
                ),
              ),
              // Exit button pinned to the bottom of the drawer
              Align(
                alignment: Alignment.bottomLeft,
                child: ListTile(
                  leading: const Icon(Icons.exit_to_app, color: Color(0xFF90CAF9)),
                  title: const Text('Exit', style: TextStyle(color: Color(0xFF90CAF9))),
                  onTap: () {
                    Navigator.pop(context); // Close the drawer first
                    // Show a confirmation dialog before exiting
                    showDialog(
                      context: context,
                      builder: (BuildContext context) {
                        return AlertDialog(
                          backgroundColor: const Color(0xFF23272A), // Match app theme
                          // Center the title text
                          title: const Center(
                            child: Text(
                              'Close Application?',
                              style: TextStyle(color: Color(0xFF90CAF9)),
                              textAlign: TextAlign.center,
                            ),
                          ),
                          content: const SizedBox.shrink(), // No extra content, just the title and buttons
                          actionsPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8), // Less horizontal padding
                          actions: [
                            // Row for side-by-side buttons, closer together and centered
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                // Yes button (on the left)
                                ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.blue[300],
                                    foregroundColor: Colors.black,
                                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                                  ),
                                  onPressed: () {
                                    Navigator.of(context).pop(); // Close the dialog
                                    SystemNavigator.pop(); // Exit the app
                                  },
                                  child: const Text('Yes'),
                                ),
                                const SizedBox(width: 36), // Small space between buttons
                                // No button (on the right)
                                ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.grey[700],
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                                  ),
                                  onPressed: () {
                                    Navigator.of(context).pop(); // Just close the dialog
                                  },
                                  child: const Text('No'),
                                ),
                              ],
                            ),
                          ],
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
      appBar: AppBar(
        // The menu icon (hamburger) is automatically shown when a drawer is present
        title: const Text('MTG Creature Type Generator', textAlign: TextAlign.center),
        centerTitle: true,
      ),
      body: _isLoading
          // Show a loading spinner while loading creature types
          ? const Center(child: CircularProgressIndicator())
          // Main content of the app
          : Stack(
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    const SizedBox(height: 24), // Spacer at the top
                    // Make the Generate Creature Type button bigger using SizedBox and style
                    SizedBox(
                      width: double.infinity,
                      height: 60,
                      child: ElevatedButton(
                        onPressed: _generateCreatureType,
                        style: ElevatedButton.styleFrom(
                          textStyle: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                          backgroundColor: Colors.blue[300],
                          foregroundColor: Colors.black,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                        child: const Text('Generate Creature Type'),
                      ),
                    ),
                    // Expanded widget to push the most recent creature text to the vertical center
                    Expanded(
                      child: Center(
                        child: _history.isNotEmpty
                            ? Text(
                                _history.first, // Most recent creature
                                style: const TextStyle(
                                  fontSize: 28,
                                  fontWeight: FontWeight.bold,
                                  color: Color.fromARGB(255, 58, 114, 183), // Stand-out color for the creature
                                ),
                                textAlign: TextAlign.center,
                              )
                            : const SizedBox.shrink(), // Empty widget if no history
                      ),
                    ),
                    // Move the history box up to make space for the New Game button
                    Padding(
                      padding: const EdgeInsets.only(bottom: 70.0), // Leave space for the floating button
                      child: CreatureHistoryBox(history: _history),
                    ),
                  ],
                ),
              ),
              // Place the New Game button at the bottom right using Positioned and Align
              Positioned(
                bottom: 20,
                right: 20,
                child: FloatingActionButton.extended(
                  onPressed: _newGame,
                  backgroundColor: Colors.blue[300],
                  foregroundColor: Colors.black,
                  icon: const Icon(Icons.refresh),
                  label: const Text(
                    'New Game',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ],
          ),
    );
  }
}

// Widget that displays the history of generated creatures in a styled box
class CreatureHistoryBox extends StatelessWidget {
  final List<String> history; // List of generated creatures

  const CreatureHistoryBox({super.key, required this.history});

  @override
  Widget build(BuildContext context) {
    // Use a slightly lighter grey than the scaffold background for contrast
    // Scaffold background is #23272A, so we'll use #2C2F33 (as in the app bar) or Colors.grey[850]
    return Container(
      width: double.infinity, // Take up all available width
      constraints: const BoxConstraints(
        minHeight: 120,
        maxHeight: 240, // Limit the height of the box
      ),
      padding: const EdgeInsets.all(16), // Padding inside the box
      decoration: BoxDecoration(
        color: const Color(0xFF2C2F33), // Slightly lighter dark grey for contrast
        borderRadius: BorderRadius.circular(12), // Rounded corners
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Title for the history section
          const Text(
            'History:',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8), // Space below the title
          // Scrollable list of generated creatures, or a message if empty
          Expanded(
            child: history.isEmpty
                ? const Center(child: Text('No creatures generated yet.'))
                : ListView.separated(
                    itemCount: history.length,
                    // Lower the vertical padding to compensate for the divider's height (1px)
                    padding: EdgeInsets.zero,
                    itemBuilder: (context, index) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 3), // Slightly reduced padding
                        child: Text(
                          history[index],
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            color: Color(0xFF90CAF9), // Use the lighter blue for text
                          ),
                        ),
                      );
                    },
                    separatorBuilder: (context, index) => const Divider(
                      color: Color(0x3390CAF9), // Feint blue line (20% opacity)
                      thickness: 1,
                      height: 1, // No extra space added by the divider
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}
