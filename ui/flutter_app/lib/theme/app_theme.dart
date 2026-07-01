import 'package:flutter/material.dart';

class AppColors {
  // Main colors
  static const Color primary = Color(0xFF1f6f3b);      // Dark green
  static const Color background = Color(0xFFf7efe2);   // Cream
  static const Color accent = Color(0xFF8b5a3c);       // Ochre/Maroon
  
  // Grays
  static const Color dark = Color(0xFF1a1a1a);
  static const Color light = Color(0xFFffffff);
  static const Color gray = Color(0xFF757575);
  static const Color lightGray = Color(0xFFe0e0e0);
  
  // Status
  static const Color success = Color(0xFF4caf50);
  static const Color error = Color(0xFFf44336);
  static const Color warning = Color(0xFFff9800);
}

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.background,
      colorScheme: ColorScheme.light(
        primary: AppColors.primary,
        secondary: AppColors.accent,
        surface: AppColors.background,
        error: AppColors.error,
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.light,
        elevation: 0,
        centerTitle: true,
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.dark,
      colorScheme: ColorScheme.dark(
        primary: AppColors.primary,
        secondary: AppColors.accent,
        surface: Color(0xFF2a2a2a),
        error: AppColors.error,
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.light,
        elevation: 0,
        centerTitle: true,
      ),
    );
  }
}
