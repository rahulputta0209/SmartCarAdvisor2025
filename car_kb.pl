% ============================
% SmartCar Advisor Knowledge Base (Rules)
% ============================

% Helper: substring match
contains(Sub, Text) :-
    atom(Sub), atom(Text),
    sub_atom(Text, _, _, _, Sub).

% --- Main Recommendation Rules ---
recommend(Car) :-
    preference(budget, B),
    preference(fuel, F),
    preference(purpose, P),
    preference(transmission, T),
    car(Car, _, price(Price), fuel(Fuel), transmission(Trans), _, purpose(Purpose), _),
    contains(F, Fuel),
    contains(T, Trans),
    contains(P, Purpose),
    Price =< B.

recommend(Car) :-
    preference(budget, B),
    preference(fuel, F),
    preference(transmission, T),
    car(Car, _, price(Price), fuel(Fuel), transmission(Trans), _, _, _),
    contains(F, Fuel),
    contains(T, Trans),
    Price =< B.

% --- Unique recommendation (group by name) ---
unique_recommend(CarList) :-
    setof(Name, (
        recommend(Name),
        \+ (recommend(Other), Name \= Other, Name @< Other)
    ), RawList),
    list_to_set(RawList, CarList), !.
unique_recommend([]).

% --- Better Explanation Predicate ---
explain(Car, Reason) :-
    car(Car, brand(Brand0), price(Price), fuel(Fuel), transmission(Trans),
        seats(Seats), purpose(Purpose), rating(Rating)),
    % Capitalize brand name
    atom_chars(Brand0, Chars),
    (Chars = [H|T] -> char_type(HU, to_upper(H)), HUChars = [HU|T], atom_chars(Brand, HUChars); Brand = Brand0),
    % Describe fuel type
    ( Fuel = electric -> FuelDesc = "an all-electric vehicle offering eco-friendly performance and zero emissions";
      Fuel = hybrid -> FuelDesc = "a hybrid model combining fuel efficiency and responsive power";
      Fuel = diesel -> FuelDesc = "a diesel engine car known for long-distance efficiency and high torque";
      Fuel = petrol -> FuelDesc = "a petrol car known for smooth acceleration and low maintenance";
      FuelDesc = "a refined engine with balanced performance"
    ),
    % Describe purpose
    ( Purpose = family -> PurposeDesc = "ideal for family trips and everyday comfort";
      Purpose = city -> PurposeDesc = "perfect for city driving, offering nimble control and compact design";
      Purpose = offroad -> PurposeDesc = "built for off-road performance and adventurous journeys";
      PurposeDesc = "versatile for various driving needs"
    ),
    % Compose final sentence
    format(string(Reason),
        "~w by ~w is a ~w-seater ~w car with ~w. It features a ~w transmission and is ~w. Priced around $~w with a ~w⭐ rating, it stands out as a great option for your needs.",
        [Car, Brand, Seats, Fuel, FuelDesc, Trans, PurposeDesc, Price, Rating]).
