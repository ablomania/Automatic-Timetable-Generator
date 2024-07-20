import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from '../screens/home-screen';
import DetailScreen from '../screens/schedules/details';
import { navOptions } from './options';
import { NavigationContainer, useNavigation } from '@react-navigation/native';
import ProfileScreen from '../screens/profiles/profiles-screen';
import ProfileDetailScreen from '../screens/profiles/profile-detail';
import HomeTabs from './tabs';
import ScheduleScreen from '../screens/schedule-screen';
import Details from '../Details';
import ScheduleDaysScreen from '../screens/schedules/days';
import SignIn from '../screens/sign-in-screen';

const Stack = createStackNavigator();

export const HomeStack = () => {
  const navigation = useNavigation()
  return (
      <Stack.Navigator>
        <Stack.Screen options={{
          title: "Home"
        }} name="HomeScreenStack" component={HomeScreen} />

      </Stack.Navigator>

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
  );
}

export const ScheduleStack = () => {
  const navigation = useNavigation();
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

export const ProfileStack = () => {
  const navigation = useNavigation()
  return (
    <Stack.Navigator>
      {/* <Stack.Screen name='SignInStack' options={{
        title: "Sign In", */}
      {/* }} component={SignIn} /> */}
      <Stack.Screen options={{
        title: 'Profile'
      }} name="ProfilesStackScreen" component={ProfileScreen} />
      <Stack.Screen options={{
        title:'About'
      }} name="ProfileStackDetail" component={ProfileDetailScreen} />
    </Stack.Navigator>
  );
}