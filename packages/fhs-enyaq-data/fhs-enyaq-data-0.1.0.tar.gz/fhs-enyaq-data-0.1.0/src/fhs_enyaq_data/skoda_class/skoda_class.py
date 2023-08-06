#!/usr/bin/env python3
from pprint import pprint
import asyncio
import inspect
import time
import sys
import os
import yaml
from aiohttp import ClientSession
from datetime import datetime


try:
    from skodaconnect import Connection
except ModuleNotFoundError as e:
    print(f"Unable to import library: {e}")
    sys.exit(1)


class skoda_class:
    def __init__(self, config=None, config_file=".skoda.cfg", verbose=False):
        self.conn = None
        self.loop = asyncio.get_event_loop()
        self.state = {}
        if config is not None:
            self.state = config
        else:
            self.config_file = config_file
            self.get_config()
        if verbose:
            self.state["verbose"] = True
        else:
            self.state["verbose"] = False

    def get_config(self):
        try:
            with open(self.config_file, "r") as file:
                self.state = yaml.load(file, Loader=yaml.FullLoader)
        except Exception as e:
            print(f"can't open config file: {self.config_file}  {e}")

    async def login_and_get_vehicles(self):
        """Main method."""
        session = ClientSession(headers={"Connection": "keep-alive"})
        if self.state.get("verbose"):
            print(
                f"Initiating new session to Skoda Connect with {self.state['username']} as username"
            )
        connection = Connection(
            session, self.state["username"], self.state["password"], False
        )
        if self.state.get("verbose"):
            print("Attempting to login to the Skoda Connect service")
            print(datetime.now())
        if await connection.doLogin():
            if self.state.get("verbose"):
                print("Login success!")
                print(datetime.now())
                print("Fetching vehicles associated with account.")
            await connection.get_vehicles()
            return (session, connection.vehicles)
        return (session, None)

    async def async_get_vehicle(self, vehicle_vin):
        (session, vehicles) = await self.login_and_get_vehicles()
        if vehicles == None:
            print("no vehicle found to set temp.")
            await session.close()
            return (None, None)
        if vehicle_vin == None:
            if len(vehicles) > 1:
                print("multiple vehicles found, please select one using vin.")
                await session.close()
                return (None, None)
            return (session, vehicles[0])
        for vehicle in vehicles:
            if vehicle_vin == vehicle.vin:
                return (session, vehicle)
        await session.close()
        return (None, None)

    async def async_get_instruments(self, vehicle_vin):
        """Async airco."""
        (session, vehicle) = await self.async_get_vehicle(vehicle_vin)
        if vehicle == None:
            print("no vehicle found.")
            await session.close()
            return None
        dashboard = vehicle.dashboard()
        instruments = dashboard.instruments
        await session.close()
        return instruments


    async def async_print_instruments(self, vehicle_vin):
        # Battery level
        instruments = await self.async_get_instruments(vehicle_vin)
        if instruments == None:
            print('no instruments')
        for i in instruments:
            print(f"{i.name} = {i.state}")
        return None

    def print_instruments(self, vehicle_vin=None):
        return self.loop.run_until_complete(
            self.async_print_instruments(vehicle_vin)
        )


    async def async_get_battery_level(self, vehicle_vin):
        # Battery level
        instruments = await self.async_get_instruments(vehicle_vin)
        if instruments == None:
            return None
        for i in instruments:
            if i.name == "Battery level":
                return int(i.state)
        return None


    def get_battery_level(self, vehicle_vin=None):
        return self.loop.run_until_complete(
            self.async_get_battery_level(vehicle_vin)
        )

    def get_instruments(self, vehicle_vin=None):
        result = self.loop.run_until_complete(
            self.async_get_instruments(vehicle_vin)
        )
        instruments={}
        for i in result:
            instruments[i.name] = i.state
        return instruments

    async def async_list_cars(self):
        """Async airco."""
        (session, vehicles) = await self.login_and_get_vehicles()
        if vehicles == None:
            print("no vehicle found.")
            await session.close()
            return False
        for vehicle in vehicles:
            print(f"VIN: {vehicle.vin}\t: {vehicle.model}")
        await session.close()


    def list_cars(self):
        print(f"listing cars")
        return self.loop.run_until_complete(self.async_list_cars())
