import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TextInput, View, Platform, Button, ScrollView, SafeAreaView, TouchableOpacity } from 'react-native';
import { useState} from "react";
import { NavigationContainer } from '@react-navigation/native';
import { HomeStack } from './navigation/stack';
import 'react-native-gesture-handler';
import MyDrawer from './navigation/drawer';
import HomeTabs from './navigation/tabs';

export default function App() {
  const [userName , setUserName] = useState("");
  const [yearGroup, setYearGroup] = useState("");
  const [college, setCollege] = useState("");
  const [departmentName, setDepartmentName] = useState("");
  var displaySignin = true;
  if(displaySignin)
    return(
        <SafeAreaView>
            <View>
                <Text>Name</Text>
                <TextInput
                onChangeText={setUserName}
                value={userName}
                style={styles.input}
                 />
                <Text>Year Group</Text>
                <TextInput
                  onChangeText={setYearGroup}
                  value={yearGroup}
                  style={styles.input}
                />
                <Text>College</Text>
                <TextInput 
                  onChangeText={setCollege}
                  value={college}
                  style={styles.input}
                />
                <Text>Department</Text>
                <TextInput
                  onChangeText={setDepartmentName}
                  value={departmentName}
                  style={styles.input}
                 />
                <Button
                onPress={() => console.log("Hello")}
                title='Continue'
                />
            </View>
        </SafeAreaView>
    )
  else
    return (
      <NavigationContainer>
        {/* <HomeStack /> */}
        <HomeTabs />
        <StatusBar style='light' />
      </NavigationContainer>
    );
}

const styles = StyleSheet.create({
  input: {
    height: 40,
    margin: 12,
    borderWidth:1,
    borderColor: "blue",
    padding: 10,
  }
})