import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from '../screens/home-screen';
import DetailScreen from '../screens/schedules/details';
import { useNavigation } from '@react-navigation/native';
import ProfileScreen from '../screens/profiles/profiles-screen';
import ProfileDetailScreen from '../screens/profiles/profile-detail';
import ScheduleScreen from '../screens/schedule-screen';
import ScheduleDaysScreen from '../screens/schedules/days';
import SignIn from '../screens/sign-in-screen';
import SignIn2 from '../screens/signin2';
import { useEffect, useState } from 'react';
import HomeTabs from './tabs';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Stack = createStackNavigator();

export function SignInStacks() {
  <Stack.Navigator screenOptions={{headerShown: false}}>
    <Stack.Screen name='SignInStack1' options={{
      title: "Sign In"}} component={SignIn}/>
    <Stack.Screen name='SignInStack2' options={{
      title: "More Info",}} component={SignIn2} />
  </Stack.Navigator>
}



export const HomeStack = ({navigation}) => {
  
  return (
    <Stack.Navigator>
      <Stack.Screen options={{
        title: "Home"
      }} name="HomeScreenStack" component={HomeScreen} />
    </Stack.Navigator>
  )
    // <Stack.Navigator
    // screenOptions={{
    //   // ()=> navOptions(navigation)
    //   headerShown: false,
    // }}
    // >
    //   <Stack.Screen name="HomeTabs"
    //     options={{
    //       title: "Home"
    //     }}
    //     component={HomeTabs} 
    //    />
    //   {/* <Stack.Screen name="Details" component={DetailScreen} /> */}
    // </Stack.Navigator>
  
}

export const ScheduleStack = ({navigation}) => {
  return (
    <Stack.Navigator>
      <Stack.Screen options={{
        title: "Days",
      }} name="ScheduleDays" component={ScheduleDaysScreen} />
      <Stack.Screen options={{
        title: "Schedules",
      }} name='SchedulesScreenStack' component={ScheduleScreen} />
      <Stack.Screen options={{
        title: "Schedule Details",
      }} name='SchDetailsStack' component={DetailScreen} />
    </Stack.Navigator>

  );
}

export const ProfileStack = ({navigation}) => {
  return (
    <Stack.Navigator>
      <Stack.Screen options={{
        title: 'Profile'
      }} name="ProfilesStackScreen" component={ProfileScreen} />
      <Stack.Screen options={{
        title:'About'
      }} name="ProfileStackDetail" component={ProfileDetailScreen} />
    </Stack.Navigator>
  );
}


      