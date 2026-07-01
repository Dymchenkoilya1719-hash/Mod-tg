import 'package:flutter/material.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const TGModApp());
}

class TGModApp extends StatelessWidget {
  const TGModApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TG Mod',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.dark,
      home: const Scaffold(
        body: Center(
          child: Text('TG Mod - Coming Soon!'),
        ),
      ),
    );
  }
}
