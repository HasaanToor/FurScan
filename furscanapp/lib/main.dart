import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:tflite_flutter/tflite_flutter.dart';

void main() {
  runApp(MaterialApp(
    home: ImageClassifierApp(),
  ));
}

class ImageClassifierApp extends StatefulWidget {
  @override
  _ImageClassifierAppState createState() => _ImageClassifierAppState();
}

class _ImageClassifierAppState extends State<ImageClassifierApp> {
  late Interpreter _interpreter;
  late List<List<double>> _output;
  late String _classificationResult;

  @override
  void initState() {
    super.initState();
    _loadModel();
    _output = List.filled(1, []);
    _classificationResult = 'No classification yet';
  }

  Future<void> _loadModel() async {
    String modelPath = 'assets/model.tflite';
    _interpreter = await Interpreter.fromAsset(modelPath);
  }

  Future<void> _classifyImage(Uint8List imageBytes) async {
    _interpreter.run(imageBytes, _output);
    List<double> predictions = _output[0];

    // Replace this with your logic to interpret the predictions
    // For simplicity, we are just printing them to the console
    print(predictions);

    // Update the UI with the classification result
    setState(() {
      _classificationResult = 'Classification Result: $predictions';
    });
  }

  Future<void> _pickImage() async {
    final ImagePicker _picker = ImagePicker();
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);

    if (image == null) return;

    List<int> imageBytes = await image.readAsBytes();
    await _classifyImage(Uint8List.fromList(imageBytes));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'FurScan',
          style: TextStyle(
            color: Colors.white, // Title text color
            fontWeight: FontWeight.bold,
            fontSize: 20.0,
          ),
        ),
        centerTitle: true, // Center the title horizontally
        backgroundColor: Colors.blue, // Background color of the AppBar
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                border: Border.all(),
              ),
              child: Center(
                child: Text(
                  'Display Image Here',
                  style: TextStyle(fontSize: 16),
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                await _pickImage();
              },
              child: Text('Pick Image from Gallery'),
            ),
            SizedBox(height: 20),
            Text(
              _classificationResult,
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}
