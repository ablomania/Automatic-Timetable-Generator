import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TextInput, View, Platform, Button, ScrollView, SafeAreaView, TouchableOpacity } from 'react-native';
import * as React from "react";
import { NavigationContainer } from '@react-navigation/native';
import { HomeStack } from './navigation/stack';
import 'react-native-gesture-handler';
import MyDrawer from './navigation/drawer';

export default function App() {
  return (
    <NavigationContainer>
      {/* <HomeStack /> */}
      <MyDrawer />
      <StatusBar style='light' />
    </NavigationContainer>
  );
}