function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESCENT(X, y, theta, alpha, num_iters) updates theta by 
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
p=size(theta);
J_history = zeros(num_iters, 1);
T=zeros(m,1);
for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta. 
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCost) and gradient here.
    %


   
%theta=theta-(alpha/m)*sum(X*theta-y);
%for i = 1:m
 %   c=0;
  %  for j=1:p
   %     c=c+(X(i,:)*theta-y(i))*X(i,j);
    %T(i)=(alpha/m)*c;
%end
%for i=1:p
 %   theta(i)=theta(i)-T(i);
%end
 % Calcul de la prédiction h(x) pour chaque point de données
        h = X * theta;
        
        % Calcul de la différence entre la prédiction et les valeurs réelles
        diff = h - y;
        
        % Mise à jour des paramètres theta
        theta = theta - (alpha/m) * (X' * diff);



    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCost(X, y, theta);
    disp(J_history(iter));

end

end
